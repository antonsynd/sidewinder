#!/usr/bin/env python3
import argparse
from io import StringIO
from pathlib import Path
from typing import Optional

import antlr4.tree.Tree
from antlr4 import ParserRuleContext
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

    dot: Digraph = antlr_tree_to_dot(tree=parse_tree, parser=parser)
    dot.render(outfile=output_path, format="png")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-i", "--input", type=Path, required=True)
    parser.add_argument("-o", "--output", type=Path, required=True)

    return parser.parse_args()


def antlr_tree_to_dot(tree: FileInputContext, parser: PythonParser, dot: Optional[Digraph] = None):
    if not dot:
        dot = Digraph()

    label: str = tree.getText()
    if not label:
        label = "<empty>"

    if isinstance(tree, ParserRuleContext):
        rule_index: int = tree.getRuleIndex()
        rule_name: str = parser.ruleNames[rule_index] if rule_index >= 0 else "<unknown_rule>"
        label += f"\nRule: {rule_name}"

    if isinstance(tree, antlr4.tree.Tree.TerminalNodeImpl):
        dot.node(name=str(id(tree)), label=label)
    else:
        dot.node(name=str(id(tree)), label=label)

        for child in tree.getChildren():
            dot.edge(tail_name=str(id(tree)), head_name=str(id(child)))
            antlr_tree_to_dot(tree=child, parser=parser, dot=dot)

    return dot


if __name__ == "__main__":
    main()
