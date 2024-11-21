from typing import MutableSequence, Optional

from antlr4 import ParseTreeWalker
from PythonParser import PythonParser
from PythonParserListener import PythonParserListener

from sidewinder.compiler_toolchain.antlr.ast_context import Context, ContextFactory, NodeName
from sidewinder.compiler_toolchain.ast import Node as ASTNode
from sidewinder.compiler_toolchain.ast_builder import ASTBuilderBase
from sidewinder.compiler_toolchain.parser import ParseTreeNode


class AntlrASTBuilder(ASTBuilderBase, PythonParserListener):
    def __init__(self):
        super().__init__()
        self._ast: Optional[ASTNode] = None
        self._ctx_stack: MutableSequence[Context] = []

    def generate_ast(self, parse_tree: ParseTreeNode) -> ASTNode:
        walker = ParseTreeWalker()
        walker.walk(listener=self, t=parse_tree)

        if not self._ast:
            raise Exception("Failed to generate an AST")

        return self._ast

    def handle_rule(self, node_name: NodeName, node_text: str) -> None:
        # Have the latest context to handle the incoming ASTNode
        # If it returns a new context, then push that context onto the stack
        # and have it handle the incoming ASTNode
        new_ctx: Optional[Context] = self._ctx_stack[-1].handle(name=node_name, text=node_text)

        if new_ctx:
            # Push new context to stack
            self._ctx_stack.append(new_ctx)

            # Pass handling to newly returned context via recursion
            self.handle_rule(node_name=node_name, node_text=node_text)

    def ensure_top_level_context(self, node_name: NodeName) -> None:
        if not self._ctx_stack:
            new_ctx: Optional[Context] = ContextFactory.build_context_for(
                node_name=node_name, top_level=True
            )

            if not new_ctx:
                raise ValueError(f"ASTNode with name {node_name.name} is not supported")

            self._ctx_stack.append(new_ctx)

    def finish_rule(self, node_name: NodeName) -> None:
        if node_name != self._ctx_stack[-1].node_name():
            return

        new_node: Optional[ASTNode] = self._ctx_stack[-1].flush()

        self._ctx_stack.pop(-1)

        if new_node and self._ctx_stack:
            # If there is still a context on the stack, have it accept the new
            # ASTNode
            self._ctx_stack[-1].accept(ASTNode=new_node)
        else:
            # Otherwise, we are done, the returned ASTNode is the root
            self._ast = new_node

    def enterEveryRule(self, ctx: ParseTreeNode):
        node_text: str = ctx.getText()
        node_rule: str = PythonParser.ruleNames[ctx.getRuleIndex()]
        node_name: NodeName = NodeName.from_str(node_rule)

        # Make sure that there is at least a top-level context
        self.ensure_top_level_context(node_name=node_name)

        # Call the implementation function on the current ASTNode
        self.handle_rule(node_name=node_name, node_text=node_text)

    def exitEveryRule(self, ctx: ParseTreeNode):
        node_rule: str = PythonParser.ruleNames[ctx.getRuleIndex()]
        node_name: NodeName = NodeName.from_str(node_rule)

        # Call implementation function with the ASTNode name
        self.finish_rule(node_name=node_name)
