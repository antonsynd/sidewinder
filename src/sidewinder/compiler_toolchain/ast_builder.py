from io import TextIOBase

from sidewinder.compiler_toolchain.ast import Node


class ASTBuilderBase:
    def __init__(self):
        pass

    def generate_ast(self, input: TextIOBase) -> Node:
        raise NotImplementedError()
