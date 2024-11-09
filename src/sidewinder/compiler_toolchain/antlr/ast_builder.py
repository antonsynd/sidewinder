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
        parse_tree = self._postprocess_parse_tree(parse_tree=parse_tree)

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

    def _postprocess_parse_tree(self, parse_tree: FileInputContext) -> FileInputContext:
        parse_tree = self._prune_empty_nodes(node=parse_tree)

        return self._simplify_direct_lineages(node=parse_tree)

    def _prune_empty_nodes(self, node: FileInputContext) -> FileInputContext:
        # Ignore empty nodes
        if not node.getText().strip():
            return None

        num_children: int = node.getChildCount()

        if num_children > 0:
            pruned_children: MutableSequence[FileInputContext] = []

            for child in node.getChildren():
                pruned_child: FileInputContext = self._prune_empty_nodes(node=child)

                # Keep a child if it was retained
                if pruned_child:
                    pruned_children.append(pruned_child)

            # Update children to only include pruned children
            node.children = pruned_children

        return node

    def _simplify_direct_lineages(
        self, node: FileInputContext, keep_first_single_child: bool = True
    ) -> FileInputContext:
        num_children: int = node.getChildCount()

        if num_children == 0:
            # Always return terminal nodes
            return node

        if num_children == 1:
            child: FileInputContext = node.getChild(0)

            # Prune the child node, but don't keep it unless it is the parent of
            # a terminal node
            pruned_child: FileInputContext = self._simplify_direct_lineages(
                node=child, keep_first_single_child=False
            )
            assert pruned_child

            node.children = [pruned_child]
        else:
            pruned_children: MutableSequence[FileInputContext] = []

            # Recursively prune each child node
            for child in node.getChildren():
                # Reset keep first single child for new lineages of nodes
                pruned_child: FileInputContext = self._simplify_direct_lineages(
                    node=child, keep_first_single_child=True
                )

                # Keep a child if it was retained
                if pruned_child:
                    pruned_children.append(pruned_child)

            # Update children to only include pruned children
            node.children = pruned_children

        # Update count after pruning
        num_children: int = node.getChildCount()
        assert num_children

        if num_children == 1:
            child: FileInputContext = node.getChild(0)

            # If this is the first node in a single lineage, or its child is terminal
            # keep it
            if keep_first_single_child or child.getChildCount() == 0:
                return node
            else:
                # Otherwise get the child directly
                return child
        # Else
        return node

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
