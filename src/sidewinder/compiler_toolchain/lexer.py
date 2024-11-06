# Write compiler in Python 3, then rewrite as Sidewinder, then it becomes
# self-hosting

# https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl01.html
"""
def fib(x: int) -> int:
    if x < 3:
        return 1
    else:
        return fib(x - 1) + fib(x - 2)
"""

"""
extern sin(arg: float) -> float
extern cos(arg: float) -> float
extern atan2(arg1: float, arg2: float) -> float

atan2(sin(0.4), cos(42))
"""
from io import StringIO, TextIOBase
from typing import Optional

from sidewinder.compiler_toolchain.token import Token


class Lexer:
    def __init__(self, buffer: TextIOBase) -> None:
        self._input_buffer: TextIOBase = buffer
        self._identifier_buffer = StringIO()
        self._emitted_eof: bool = False

    def try_get_next_character(self) -> Optional[str]:
        c: str = self._input_buffer.read(1)

        return c if c else None

    def try_get_next_token(self) -> Optional[Token]:
        last_char: Optional[str] = None

        # Skip any whitespace
        # TODO: treat whitespace indentation as Python would
        while last_char and last_char.isspace():
            last_char = self.try_get_next_character()

        if not last_char:
            if self._emitted_eof:
                self._emitted_eof = True
                return None
            else:
                return Token(token_type=Token.Type.EOF)

        if last_char.isalpha():  # TODO: allow underscore
            # [a-zA-Z][a-zA-Z0-9]*
            while last_char and last_char.isalnum():
                self._identifier_buffer.write(last_char)
                last_char = self.try_get_next_character()

            identifier_str: str = self._identifier_buffer.getvalue()
            token_type: Token.Type = Token.Type.from_str(s=identifier_str)

            self._identifier_buffer.truncate(0)

            if token_type == Token.Type.IDENTIFIER:
                return Token(token_type=token_type, value=identifier_str)
            else:
                return Token(token_type=token_type)

        if last_char.isdigit() or last_char == ".":
            str_val = StringIO()

            # TODO: Make this more robust
            while last_char and last_char.isdigit() or last_char == ".":
                str_val.write(last_char)
                last_char = self.try_get_next_character()

            return Token(token_type=Token.Type.NUMBER, value=float(str_val))

        if last_char == "#":
            while last_char and last_char != "\n" and last_char != "\r":
                last_char = self.try_get_next_character()

            # Ignore comments, skip to next token
            return self.try_get_next_token()
