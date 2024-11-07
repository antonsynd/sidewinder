#!/usr/bin/env python3
import argparse
from io import StringIO
from pathlib import Path

from sidewinder.compiler_toolchain.lexer import Lexer
from sidewinder.compiler_toolchain.parser import Parser


def main() -> None:
    args = parse_args()

    input_path: Path = args.input
    input_buffer = StringIO(input_path.read_text())
    lexer = Lexer(buffer=input_buffer)
    parser = Parser(lexer=lexer)
    parser.parse()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-i", "--input", type=Path, required=True)

    return parser.parse_args()


if __name__ == "__main__":
    main()
