#!/usr/bin/env python3
import argparse
from io import StringIO
from pathlib import Path

from PythonParser import PythonParser

from sidewinder.compiler_toolchain.antlr.ast_builder import AntlrASTBuilder
from sidewinder.compiler_toolchain.antlr.parser import AntlrParser
from sidewinder.compiler_toolchain.ast import Node
from sidewinder.compiler_toolchain.parser import ParseTreeNode


def main() -> None:
    args = parse_args()

    input_path: Path = args.input
    input_buffer = StringIO(input_path.read_text())

    antlr_builder = AntlrParser()
    parser: PythonParser = antlr_builder._create_parser(input=input_buffer)
    parse_tree: ParseTreeNode = parser.file_input()
    parse_tree = antlr_builder._postprocess_parse_tree(parse_tree=parse_tree)
    ast_builder = AntlrASTBuilder()
    node: Node = ast_builder.generate_ast(parse_tree=parse_tree)

    print(f"Resulting AST: {node}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-i", "--input", type=Path, required=True)

    return parser.parse_args()


if __name__ == "__main__":
    main()
