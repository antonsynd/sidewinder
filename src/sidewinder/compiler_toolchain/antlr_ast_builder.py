from io import TextIOBase
from typing import Optional, Sequence

from antlr4 import CommonTokenStream, InputStream, ParseTreeWalker
from PythonLexer import PythonLexer
from PythonParser import PythonParser
from PythonParserListener import PythonParserListener


class CustomASTNode:
    def __init__(self, name: str, children: Optional[Sequence["CustomASTNode"]] = None):
        self.name: str = name
        self.children: Sequence[CustomASTNode] = children if children else []

    def __repr__(self):
        return f"{self.name} -> ({', '.join(map(str, self.children))})"


# Step 3: Define a Listener to Build Custom AST
class ASTBuilder(PythonParserListener):
    def __init__(self):
        self.ast: Optional[CustomASTNode] = None
        self.node_stack: Sequence[CustomASTNode] = []

    def enterEveryRule(self, ctx):
        # Called when entering any rule
        node_name = PythonParser.ruleNames[ctx.getRuleIndex()]
        node = CustomASTNode(name=node_name)
        if self.node_stack:
            self.node_stack[-1].children.append(node)
        else:
            self.ast = node
        self.node_stack.append(node)

    def exitEveryRule(self, ctx):
        # Called when exiting any rule
        self.node_stack.pop()


class AntlrASTBuilder:
    def __init__(self):
        pass

    def generate_ast(input: TextIOBase) -> CustomASTNode:
        stream = InputStream(data=input.read())
        lexer = PythonLexer(input=stream)
        token_stream = CommonTokenStream(lexer=lexer)
        parser = PythonParser(input=token_stream)

        # Parse the input, starting with the 'file_input' rule
        parse_tree = parser.file_input()

        ast_builder = ASTBuilder()
        walker = ParseTreeWalker()
        walker.walk(listener=ast_builder, t=parse_tree)

        return ast_builder.ast
