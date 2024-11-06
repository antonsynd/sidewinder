#!/usr/bin/env python3
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
from enum import IntEnum, auto
from io import StringIO, TextIOBase
from typing import Mapping, Optional, Sequence


class Token(IntEnum):
    @staticmethod
    def _generate_next_value_(
        name: str, start: int, count: int, last_values: Sequence[int]
    ) -> int:
        return -1 - count

    EOF = auto()

    # Commands
    DEF = auto()
    EXTERN = auto()
    LAMBDA = auto()

    # Other keywords
    IDENTIFIER = auto()
    RETURN = auto()
    YIELD = auto()
    TRY = auto()
    EXCEPT = auto()
    FINALLY = auto()
    IF = auto()
    ELSE = auto()
    FOR = auto()
    WHILE = auto()
    IN = auto()
    ELIF = auto()
    IMPORT = auto()
    ARROW = auto()  # ->
    COMMA = auto()
    LEFT_PARENS = auto()
    RIGHT_PARENS = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    AT = auto()

    # Values
    ANNOTATION = auto()
    LITERAL_STRING = auto()
    LITERAL_NUMBER = auto()
    TRUE = auto()
    FALSE = auto()

    # Operators
    TYPE = auto()
    UNDERSCORE = auto()
    AS = auto()
    IS = auto()
    FROM = auto()
    WITH = auto()
    GLOBAL = auto()
    NONLOCAL = auto()
    PASS = auto()
    RAISE = auto()
    ASSERT = auto()
    BREAK = auto()
    CONTINUE = auto()
    AWAIT = auto()
    ASYNC = auto()
    DEL = auto()
    PLUS = auto()
    HYPHEN = auto()
    COLON = auto()
    ASTERISK = auto()
    SLASH = auto()
    PIPE = auto()
    CARET = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    CARET = auto()
    MODULUS = auto()
    EQUAL = auto()
    LESS_THAN = auto()
    GREATER_THAN = auto()
    LESS_THAN_OR_EQUAL = auto()
    GREATER_THAN_OR_EQUAL = auto()
    QUESTION_MARK = auto()
    EXPONENT = auto()
    BITWISE_LEFT_SHIFT = auto()
    BITWISE_RIGHT_SHIFT = auto()
    EQUALITY = auto()
    INEQUALITY = auto()

    # Types
    INT = auto()  # 32-bit
    NUMBER = auto()  # 64-bit
    FLOAT = auto()  # 32-bit
    DOUBLE = auto()  # 64-bit
    STR = auto()
    BOOL = auto()
    NONE = auto()
    LIST = auto()
    SET = auto()
    DICT = auto()  # always ordered
    TUPLE = auto()
    BYTES = auto()  # immutable
    BYTEARRAY = auto()  # mutable
    OPTIONAL = auto()  # or also ?

    CLASS = auto()  # regular class, mutable, by-reference
    STRUCT = auto()  # immutable class, copy-only


_string_to_token_map: Mapping[str, Token] = {
    "def": Token.DEF,
    "extern": Token.EXTERN,
    "class": Token.CLASS,
    "float": Token.FLOAT,
    "double": Token.DOUBLE,
    "int": Token.INT,
    "str": Token.STR,
    "bytes": Token.BYTES,
    "bytearray": Token.BYTEARRAY,
    "struct": Token.STRUCT,
    "lambda": Token.LAMBDA,
    "bool": Token.BOOL,
    "dict": Token.DICT,
    "set": Token.SET,
    "tuple": Token.TUPLE,
    "list": Token.LIST,
    "None": Token.NONE,
    "number": Token.NUMBER,
    "True": Token.TRUE,
    "False": Token.FALSE,
    "Optional": Token.OPTIONAL,
    "if": Token.IF,
    "else": Token.ELSE,
    "elif": Token.ELIF,
    "while": Token.WHILE,
    "for": Token.FOR,
    "finally": Token.FINALLY,
    "try": Token.TRY,
    "except": Token.EXCEPT,
    "del": Token.DEL,
    "from": Token.FROM,
    "global": Token.GLOBAL,
    "import": Token.IMPORT,
    "nonlocal": Token.NONLOCAL,
    "not": Token.NOT,
    "and": Token.AND,
    "in": Token.IN,
    "is": Token.IS,
    "or": Token.OR,
    "pass": Token.PASS,
    "raise": Token.RAISE,
    "with": Token.WITH,
    "yield": Token.YIELD,
    "async": Token.ASYNC,
    "await": Token.AWAIT,
    "type": Token.TYPE,
}


class Lexer:
    def __init__(self, buffer: TextIOBase) -> None:
        self._input_buffer: TextIOBase = buffer
        self._identifier_buffer = StringIO()
        self._num_val: float = 0.0

        self._emitted_eof: bool = False

    def try_get_next_character(self) -> Optional[str]:
        c: str = self._input_buffer.read(1)

        return c if c else None

    def get_token_type_for_string(self, s: str) -> Token:
        return _string_to_token_map.get(s, Token.IDENTIFIER)

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
                return Token.EOF

        if last_char.isalpha():  # TODO: allow underscore
            # [a-zA-Z][a-zA-Z0-9]*
            while last_char and last_char.isalnum():
                self._identifier_buffer.write(last_char)
                last_char = self.try_get_next_character()

            return self.get_token_type_for_string(s=self._identifier_buffer.getvalue())

        if last_char.isdigit() or last_char == ".":
            str_val = StringIO()

            # TODO: Make this more robust
            while last_char and last_char.isdigit() or last_char == ".":
                str_val.write(last_char)
                last_char = self.try_get_next_character()

            self._num_val = float(str_val)

            return Token.NUMBER

        if last_char == "#":
            while last_char and last_char != "\n" and last_char != "\r":
                last_char = self.try_get_next_character()

            # Ignore comments, skip to next token
            return self.try_get_next_token()
