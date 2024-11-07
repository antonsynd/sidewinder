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
        self._last_char: str = " "

    def last_char(self) -> str:
        return self._last_char

    def get_next_character(self) -> str:
        self._last_char = self._input_buffer.read(1)

        return self._last_char

    def _emit_eof(self) -> Optional[Token]:
        if self._emitted_eof:
            self._emitted_eof = True
            return None
        else:
            return Token(token_type=Token.Type.EOF)

    def try_get_next_token(self) -> Optional[Token]:
        # Skip any whitespace
        # TODO: treat whitespace indentation as Python would
        while self.last_char() and self.last_char().isspace():
            self.get_next_character()

        if not self.last_char():
            return self._emit_eof()

        if self.last_char().isalpha():  # TODO: allow underscore
            # [a-zA-Z][a-zA-Z0-9]*
            while self.last_char() and self.last_char().isalnum():
                self._identifier_buffer.write(self.last_char())
                self.get_next_character()

            identifier_str: str = self._identifier_buffer.getvalue()
            token_type: Token.Type = Token.Type.from_str(s=identifier_str)

            self._identifier_buffer.truncate(0)

            if token_type == Token.Type.IDENTIFIER:
                return Token(token_type=token_type, value=identifier_str)
            else:
                return Token(token_type=token_type)

        if self.last_char().isdigit() or self.last_char() == ".":
            str_val = StringIO()

            # TODO: Make this more robust
            while self.last_char() and self.last_char().isdigit() or self.last_char() == ".":
                str_val.write(self.last_char())
                self.get_next_character()

            return Token(token_type=Token.Type.NUMBER, value=float(str_val.getvalue()))

        if self.last_char() == "#":
            while self.last_char() and self.last_char() != "\n" and self.last_char() != "\r":
                self.get_next_character()

            # Ignore comments, skip to next token
            if self.last_char():
                return self.try_get_next_token()

        if not self.last_char():
            return self._emit_eof()

        # Unknown token
        retval = Token(token_type=Token.Type.UNK, value=self.last_char())
        self.get_next_character()

        return retval
