#!/usr/bin/env python3
import argparse
from io import StringIO
from pathlib import Path
from typing import Sequence

from sidewinder.compiler_toolchain.ast import Node
from sidewinder.compiler_toolchain.default_ast_builder import DefaultASTBuilder
from sidewinder.compiler_toolchain.default_parser import DefaultParser
from sidewinder.compiler_toolchain.parser import ParseTreeNode


def main() -> None:
    args: argparse.Namespace = parse_args()

    input_paths: Sequence[Path] = args.input_paths
    output_path: Path = args.output

    compile(input_paths=input_paths, output_path=output_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="swc: the Sidewinder compiler")
    parser.add_argument(
        "input",
        type=Path,
        dest="input_paths",
        nargs="+",
        help="Paths to the input Sidewinder *.sw source files",
    )
    parser.add_argument(
        "-o", "--output", type=Path, required=True, help="Path to the output binary file."
    )

    return parser.parse_args()


def compile(input_paths: Sequence[Path], output_path: Path) -> None:
    input_path: Path = input_paths[0]
    input_buffer = StringIO(input_path.read_text())

    parser = DefaultParser()
    parse_tree: ParseTreeNode = parser.parse(input=input_buffer)
    ast_builder = DefaultASTBuilder()
    node: Node = ast_builder.generate_ast(parse_tree=parse_tree)


if __name__ == "__main__":
    main()
