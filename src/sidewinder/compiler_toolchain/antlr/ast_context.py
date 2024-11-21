from enum import Enum, auto
from typing import Mapping, MutableSequence, Optional, Type

from sidewinder.compiler_toolchain.ast import Atom, Expression, FunctionCall, Module, Node


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


_node_name_str_to_enum_mapping: Mapping[str, NodeName] = {
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
    def __init__(self, node_name: NodeName):
        self._node_name: NodeName = node_name

    def node_name(self) -> NodeName:
        return self._node_name

    def flush(self) -> Optional[Node]:
        raise NotImplementedError()

    def handle(self, name: NodeName, text: str) -> Optional["Context"]:
        raise NotImplementedError()

    def accept(self, node: Node) -> None:
        raise NotImplementedError()

    def raise_unexpected(self, name: NodeName) -> None:
        raise ValueError(f"Unexpected node {name.name} in {self.__class__.__name__}")


class ModuleContext(Context):
    def __init__(self):
        super().__init__(node_name=NodeName.MODULE)

        self._statements: MutableSequence[Node] = []

    def handle(self, name: NodeName, text: str) -> Optional[Context]:
        if name == NodeName.MODULE:
            # No need to do anything
            return None
        elif name == NodeName.FUNCTION_CALL:
            return FunctionCallContext()

        self.raise_unexpected(name=name)

    def flush(self) -> Optional[Node]:
        module = Module()
        module.statements().extend(self._statements)

        return module

    def accept(self, node: Node) -> None:
        self._statements.append(node)


class FunctionDefContext(Context):
    pass


class AtomContext(Context):
    pass


class ReturnStatementContext(Context):
    pass


class ArgumentsContext(Context):
    def __init__(self, func: "FunctionCallContext"):
        super().__init__(node_name=NodeName.ARGUMENTS)

        self._func: FunctionCallContext = func

    def flush(self) -> Optional[Node]:
        # Do nothing, function context already has arguments
        return None

    def handle(self, name: NodeName, text: str) -> Optional[Context]:
        if name == NodeName.ARGUMENTS:
            return None
        elif name == NodeName.ATOM:
            atom = Atom()
            atom.set_name(name=text)

            self._func.arguments().append(atom)
            return None

        self.raise_unexpected(name=name)

    def accept(self, node: Node) -> None:
        pass


class FunctionCallContext(Context):
    def __init__(self):
        super().__init__(node_name=NodeName.FUNCTION_CALL)

        self._name: Optional[str] = None
        self._args: MutableSequence[Expression] = []

    def arguments(self) -> MutableSequence[Expression]:
        return self._args

    def flush(self) -> Optional[Node]:
        node = FunctionCall()
        node.set_name(self._name)
        node.arguments().extend(self._args)

        return node

    def handle(self, name: NodeName, text: str) -> Optional[Context]:
        if name == NodeName.FUNCTION_CALL:
            return None
        elif name == NodeName.ATOM:
            self._name = text

            return None
        elif name == NodeName.ARGUMENTS:
            return ArgumentsContext(func=self)

        self.raise_unexpected(name=name)

    def accept(self, node: Node) -> None:
        pass


class ContextFactory:
    _node_name_to_context_class_mapping: Mapping[NodeName, Type] = {
        NodeName.MODULE: ModuleContext,
        NodeName.FUNCTION_DEF: FunctionDefContext,
        NodeName.ATOM: AtomContext,
        NodeName.FUNCTION_CALL: FunctionCallContext,
        NodeName.ARGUMENTS: ArgumentsContext,
        NodeName.RETURN_STATEMENT: ReturnStatementContext,
    }

    _top_level_node_name_to_context_class_mapping: Mapping[NodeName, Type] = {
        NodeName.MODULE: ModuleContext,
    }

    @classmethod
    def build_context_for(cls, node_name: NodeName, top_level: bool = False) -> Optional[Context]:
        res: Optional[Type] = None

        if top_level:
            res = cls._top_level_node_name_to_context_class_mapping.get(node_name, None)
        else:
            res = cls._node_name_to_context_class_mapping.get(node_name, None)

        if not res:
            raise ValueError(f"No context for {node_name.name} with top_level = {top_level}")

        return res()
