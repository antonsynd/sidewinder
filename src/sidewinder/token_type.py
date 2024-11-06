from enum import auto, Enum
from typing import Mapping


class TokenType(Enum):
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

    @classmethod
    def from_str(cls, s: str) -> "TokenType":
        return _string_to_token_type_map.get(s, TokenType.IDENTIFIER)


_string_to_token_type_map: Mapping[str, TokenType] = {
    "def": TokenType.DEF,
    "extern": TokenType.EXTERN,
    "class": TokenType.CLASS,
    "float": TokenType.FLOAT,
    "double": TokenType.DOUBLE,
    "int": TokenType.INT,
    "str": TokenType.STR,
    "bytes": TokenType.BYTES,
    "bytearray": TokenType.BYTEARRAY,
    "struct": TokenType.STRUCT,
    "lambda": TokenType.LAMBDA,
    "bool": TokenType.BOOL,
    "dict": TokenType.DICT,
    "set": TokenType.SET,
    "tuple": TokenType.TUPLE,
    "list": TokenType.LIST,
    "None": TokenType.NONE,
    "number": TokenType.NUMBER,
    "True": TokenType.TRUE,
    "False": TokenType.FALSE,
    "Optional": TokenType.OPTIONAL,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "elif": TokenType.ELIF,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
    "finally": TokenType.FINALLY,
    "try": TokenType.TRY,
    "except": TokenType.EXCEPT,
    "del": TokenType.DEL,
    "from": TokenType.FROM,
    "global": TokenType.GLOBAL,
    "import": TokenType.IMPORT,
    "nonlocal": TokenType.NONLOCAL,
    "not": TokenType.NOT,
    "and": TokenType.AND,
    "in": TokenType.IN,
    "is": TokenType.IS,
    "or": TokenType.OR,
    "pass": TokenType.PASS,
    "raise": TokenType.RAISE,
    "with": TokenType.WITH,
    "yield": TokenType.YIELD,
    "async": TokenType.ASYNC,
    "await": TokenType.AWAIT,
    "type": TokenType.TYPE,
}
