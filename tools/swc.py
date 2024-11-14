#!/usr/bin/env python3
import argparse
from pathlib import Path

import sidewinder.compiler_toolchain


def main() -> None:
    args: argparse.Namespace = parse_args()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-i", "--input", type=Path, required=True)

    return parser.parse_args()


if __name__ == "__main__":
    main()
