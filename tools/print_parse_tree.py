#!/usr/bin/env python3
import argparse
from io import StringIO
from pathlib import Path
from typing import Optional

import antlr4.tree.Tree
from graphviz import Digraph
from PythonParser import PythonParser

from sidewinder.compiler_toolchain.antlr.ast_builder import AntlrASTBuilder, FileInputContext


def main() -> None:
    args = parse_args()

    input_path: Path = args.input
    input_buffer = StringIO(input_path.read_text())
    output_path: Path = args.output

    antlr_builder = AntlrASTBuilder()
    parser: PythonParser = antlr_builder._create_parser(input=input_buffer)
    parse_tree: FileInputContext = parser.file_input()

    dot: Digraph = antlr_tree_to_dot(tree=parse_tree)
    dot.render(outfile=output_path, format="png")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-i", "--input", type=Path, required=True)
    parser.add_argument("-o", "--output", type=Path, required=True)

    return parser.parse_args()


def antlr_tree_to_dot(tree: FileInputContext, dot: Optional[Digraph] = None):
    if not dot:
        dot = Digraph()

    if isinstance(tree, antlr4.tree.Tree.TerminalNodeImpl):
        dot.node(str(id(tree)), tree.getText())
    else:
        dot.node(str(id(tree)), tree.getText())
        for child in tree.getChildren():
            dot.edge(str(id(tree)), str(id(child)))
            antlr_tree_to_dot(child, dot)

    return dot


if __name__ == "__main__":
    main()
