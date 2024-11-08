#!/usr/bin/env python3
import argparse
from io import StringIO
from pathlib import Path

from sidewinder.compiler_toolchain.ast import ASTNode
from sidewinder.compiler_toolchain.default_ast_builder import DefaultASTBuilder


def main() -> None:
    args = parse_args()

    input_path: Path = args.input
    input_buffer = StringIO(input_path.read_text())

    builder = DefaultASTBuilder()
    res: ASTNode = builder.generate_ast(input=input_buffer)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-i", "--input", type=Path, required=True)

    return parser.parse_args()


if __name__ == "__main__":
    main()
