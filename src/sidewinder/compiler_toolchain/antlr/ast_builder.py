from io import TextIOBase
from typing import MutableSequence, Optional

from antlr4 import CommonTokenStream, InputStream, ParseTreeWalker
from PythonLexer import PythonLexer
from PythonParser import PythonParser
from PythonParserListener import PythonParserListener

from sidewinder.compiler_toolchain.ast import ASTNode
from sidewinder.compiler_toolchain.ast_builder import ASTBuilderBase

FileInputContext = PythonParser.File_inputContext


class AntlrASTBuilder(ASTBuilderBase, PythonParserListener):
    def __init__(self):
        super().__init__()
        self._ast: Optional[ASTNode] = None
        self._node_stack: MutableSequence[ASTNode] = []

    def generate_ast(self, input: TextIOBase) -> ASTNode:
        parse_tree: FileInputContext = self._generate_parse_tree(input=input)

        walker = ParseTreeWalker()
        walker.walk(listener=self, t=parse_tree)

        return self._ast

    def _create_parser(self, input: TextIOBase) -> PythonParser:
        stream = InputStream(data=input.read())
        lexer = PythonLexer(input=stream)
        token_stream = CommonTokenStream(lexer=lexer)

        return PythonParser(input=token_stream)

    def _generate_parse_tree(self, input: TextIOBase) -> FileInputContext:
        parser: PythonParser = self._create_parser(input=input)

        # Parse the input, starting with the 'file_input' rule
        return parser.file_input()

    def enterEveryRule(self, ctx: FileInputContext):
        node_name: str = PythonParser.ruleNames[ctx.getRuleIndex()]
        node = ASTNode(name=node_name)

        if self._node_stack:
            self._node_stack[-1].children.append(node)
        else:
            self._ast = node

        self._node_stack.append(node)

    def exitEveryRule(self, ctx: FileInputContext):
        self._node_stack.pop()
