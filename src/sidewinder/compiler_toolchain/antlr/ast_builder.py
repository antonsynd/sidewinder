from io import TextIOBase
from typing import MutableSequence, Optional

from antlr4 import CommonTokenStream, InputStream, ParseTreeWalker
from PythonLexer import PythonLexer
from PythonParser import PythonParser
from PythonParserListener import PythonParserListener

from sidewinder.compiler_toolchain.ast import ASTNode
from sidewinder.compiler_toolchain.ast_builder import ASTBuilderBase

FileInputContext = PythonParser.File_inputContext


class ASTBuilder(PythonParserListener):
    def __init__(self):
        self.ast: Optional[ASTNode] = None
        self.node_stack: MutableSequence[ASTNode] = []

    def enterEveryRule(self, ctx: FileInputContext):
        node_name = PythonParser.ruleNames[ctx.getRuleIndex()]
        node = ASTNode(name=node_name)
        if self.node_stack:
            self.node_stack[-1].children.append(node)
        else:
            self.ast = node
        self.node_stack.append(node)

    def exitEveryRule(self, ctx: FileInputContext):
        self.node_stack.pop()


class AntlrASTBuilder(ASTBuilderBase):
    def __init__(self):
        super().__init__()

    def generate_ast(self, input: TextIOBase) -> ASTNode:
        stream = InputStream(data=input.read())
        lexer = PythonLexer(input=stream)
        token_stream = CommonTokenStream(lexer=lexer)
        parser = PythonParser(input=token_stream)

        # Parse the input, starting with the 'file_input' rule
        parse_tree: FileInputContext = parser.file_input()

        ast_builder = ASTBuilder()
        walker = ParseTreeWalker()
        walker.walk(listener=ast_builder, t=parse_tree)

        return ast_builder.ast
