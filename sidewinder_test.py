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
from io import StringIO
from typing import Sequence

class Token(IntEnum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: Sequence[int]) -> int:
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
    STRING = auto()
    NUMBER = auto()
    TRUE = auto()
    FALSE = auto()

    # Operators
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

    # Types
    INT = auto()     # 32-bit
    NUMBER = auto()  # 64-bit
    FLOAT = auto()   # 32-bit
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


# TODO: replace with Context class
identifier_str = StringIO()
num_val: float = 0.0

def get_token() -> Token:
    global identifier_str
    global num_val

    last_char: str = ' '

    # Skip any whitespace
    # TODO: address whitespace as python would
    while last_char.isspace():
        last_char = input.get()

    if last_char.isalpha():  # identifier [a-zA-Z][a-zA-Z0-9]
        identifier_str.write(last_char)

        while last_char.isalnum():
            last_char = input.get()
            identifier_str.write(last_char)
        if identifier_str.getvalue() == "def":
            return Token.DEF
        elif identifier_str.getvalue() == "extern":
            return Token.EXTERN
        else:
            return Token.IDENTIFIER

    if last_char.isdigit() or last_char == '.':
        str_val: str = ""
        while last_char.isdigit() or last_char == '.':
            str_val += last_char
            last_char = input.get()
        num_val = float(str_val)
        return Token.NUMBER

    if last_char == '#':
        while last_char != '\n' and last_char != '\r':
            last_char = input.get()

    if last_char == EOF:
        return Token.END_OF_FILE

    return Token(last_char)
