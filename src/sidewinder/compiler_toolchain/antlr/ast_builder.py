from typing import MutableSequence, Optional

from antlr4 import ParseTreeWalker
from PythonParser import PythonParser
from PythonParserListener import PythonParserListener

from sidewinder.compiler_toolchain.ast import Node
from sidewinder.compiler_toolchain.ast_builder import ASTBuilderBase
from sidewinder.compiler_toolchain.parser import ParseTreeNode


class AntlrASTBuilder(ASTBuilderBase, PythonParserListener):
    def __init__(self):
        super().__init__()
        self._ast: Optional[Node] = None
        self._node_stack: MutableSequence[Node] = []

    def generate_ast(self, parse_tree: ParseTreeNode) -> Node:
        walker = ParseTreeWalker()
        walker.walk(listener=self, t=parse_tree)

        return self._ast

    def enterEveryRule(self, ctx: ParseTreeNode):
        node_name: str = PythonParser.ruleNames[ctx.getRuleIndex()]
        node = Node(name=node_name)

        if self._node_stack:
            self._node_stack[-1].children.append(node)
        else:
            self._ast = node

        self._node_stack.append(node)

    def exitEveryRule(self, ctx: ParseTreeNode):
        self._node_stack.pop()
