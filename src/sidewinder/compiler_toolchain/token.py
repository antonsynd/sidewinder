from typing import Optional

from sidewinder.compiler_toolchain.token_type import TokenType


class Token:
    Type = TokenType

    def __init__(self, token_type: TokenType, value: Optional[str] = None):
        self._token_type: TokenType = token_type
        self._value: Optional[str] = value

    def token_type(self) -> TokenType:
        return self._token_type

    def value(self) -> Optional[str]:
        return self._value

    def __str__(self) -> str:
        str_value: str = f"'{self._value}'" if self._value else "None"
        return f"Token(type = {self._token_type.name}, value = {str_value})"
