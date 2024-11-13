from enum import Enum, auto
from typing import Mapping, MutableSequence, Optional, Type

from antlr4 import ParseTreeWalker
from PythonParser import PythonParser
from PythonParserListener import PythonParserListener

from sidewinder.compiler_toolchain.ast import Atom, Expression, FunctionCall, Node
from sidewinder.compiler_toolchain.ast_builder import ASTBuilderBase
from sidewinder.compiler_toolchain.parser import ParseTreeNode


class NodeName(Enum):
    UNKNOWN = auto()
    MODULE = auto()
    FUNCTION_DEF = auto()
    FUNCTION_CALL = auto()
    SUM = auto()
    ASSIGNMENT = auto()
    ATOM = auto()
    RETURN_STATEMENT = auto()
    ARGUMENTS = auto()

    @classmethod
    def from_str(cls, s: str) -> "NodeName":
        return _node_name_str_to_enum_mapping.get(s, NodeName.UNKNOWN)


_node_name_str_to_enum_mapping: Mapping[str, "NodeName"] = {
    "file_input": NodeName.MODULE,
    "primary": NodeName.FUNCTION_CALL,
    "atom": NodeName.ATOM,
    "function_def_raw": NodeName.FUNCTION_DEF,
    "sum": NodeName.SUM,
    "assignment": NodeName.ASSIGNMENT,
    "return_stmt": NodeName.RETURN_STATEMENT,
    "args": NodeName.ARGUMENTS,
}


class Context:
    def flush(self, name: NodeName) -> Optional[Node]:
        raise NotImplementedError()

    def handle(self, name: NodeName, text: str, node: ParseTreeNode) -> Optional["Context"]:
        raise NotImplementedError()

    def raise_unexpected(self, name: NodeName) -> None:
        raise ValueError(f"Unexpected node {name.name} in {self.__class__.__name__}")


class ModuleContext(Context):
    def handle(self, name: NodeName, text: str, node: ParseTreeNode) -> Optional["Context"]:
        if name == NodeName.MODULE:
            # No need to do anything
            return None
        elif name == NodeName.FUNCTION_CALL:
            return FunctionCallContext()

        self.raise_unexpected(name=name)

    def flush(self, name: NodeName) -> Optional[Node]:
        pass


class FunctionDefContext(Context):
    pass


class AtomContext(Context):
    pass


# Forward decl
class FunctionCallContext(Context):
    pass


class ArgumentsContext(Context):
    def __init__(self, func: FunctionCallContext):
        super().__init__()

        self._func: FunctionCallContext = func

    def flush(self, name: NodeName) -> Optional[Node]:
        # Do nothing, function context already has arguments
        return None

    def handle(self, name: NodeName, text: str, node: ParseTreeNode) -> Optional[Context]:
        if name == NodeName.ARGUMENTS:
            return None
        elif name == NodeName.ATOM:
            atom = Atom()
            atom.set_name(name=text)

            self._func.arguments().append(atom)
            return None

        self.raise_unexpected(name=name)


class FunctionCallContext(Context):
    def __init__(self):
        super().__init__()

        self._name: Optional[str] = None
        self._args: MutableSequence[Expression] = []

    def arguments(self) -> MutableSequence[Expression]:
        return self._args

    def flush(self, name: NodeName) -> Optional[Node]:
        if name == NodeName.FUNCTION_CALL:
            node = FunctionCall()
            node.set_name(self._name)
            node.arguments().extend(self._args)

            return node

        return None

    def handle(self, name: NodeName, text: str, node: ParseTreeNode) -> Optional[Context]:
        if name == NodeName.FUNCTION_CALL:
            return None
        elif name == NodeName.ATOM:
            atom = Atom()
            atom.set_name(name=text)

            self._args.append(atom)
            return None
        elif name == NodeName.ARGUMENTS:
            return ArgumentsContext(func=self)

        self.raise_unexpected(name=name)


_node_name_to_context_class_mapping: Mapping[NodeName, Type] = {
    NodeName.MODULE: ModuleContext,
    NodeName.FUNCTION_DEF: FunctionDefContext,
    NodeName.ATOM: AtomContext,
    NodeName.FUNCTION_CALL: FunctionCallContext,
    NodeName.ARGUMENTS: ArgumentsContext,
}


_EOF: str = "EOF"


class AntlrASTBuilder(ASTBuilderBase, PythonParserListener):
    def __init__(self):
        super().__init__()
        self._ast: Optional[Node] = None
        self._ctx_stack: MutableSequence[Context] = []

    def try_create_context_for_node(
        self, node_name: NodeName, raises: bool = False
    ) -> Optional[Context]:
        res: Optional[Type] = _node_name_to_context_class_mapping.get(node_name, None)

        if not res and raises:
            raise ValueError(f"No context for {node_name.name}")

        return res()

    def generate_ast(self, parse_tree: ParseTreeNode) -> Node:
        walker = ParseTreeWalker()
        walker.walk(listener=self, t=parse_tree)

        return self._ast

    def handle_rule(self, node_name: NodeName, node_text: str, node: ParseTreeNode) -> None:
        new_ctx: Optional[Context] = self._ctx_stack[-1].handle(
            name=node_name, text=node_text, node=node
        )

        if new_ctx:
            self._ctx_stack.append(new_ctx)

            # Recursive to pass handling to next context
            self.handle_rule(node_name=node_name, node_text=node_text, node=node)

    def ensure_top_level_context(self, node_name: NodeName) -> None:
        if not self._ctx_stack:
            new_ctx: Optional[Context] = self.try_create_context_for_node(node_name=node_name)

            if not new_ctx:
                raise ValueError(f"Node with name {node_name.name} is not supported")

            self._ctx_stack.append(new_ctx)

    def enterEveryRule(self, ctx: ParseTreeNode):
        node_text: str = ctx.getText()
        node_rule: str = PythonParser.ruleNames[ctx.getRuleIndex()]
        node_name: NodeName = NodeName.from_str(node_rule)

        self.ensure_top_level_context(node_name=node_name)
        self.handle_rule(node_name=node_name, node_text=node_text, node=ctx)

    def exitEveryRule(self, ctx: ParseTreeNode):
        node_rule: str = PythonParser.ruleNames[ctx.getRuleIndex()]
        node_name: NodeName = NodeName.from_str(node_rule)
        new_node: Optional[Node] = self._ctx_stack[-1].flush(name=node_name)

        if new_node:
            self._ctx_stack.pop(-1)
