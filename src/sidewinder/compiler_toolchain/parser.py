import sys
from typing import Any, Optional

from sidewinder.compiler_toolchain.lexer import Lexer
from sidewinder.compiler_toolchain.token import Token
from sidewinder.compiler_toolchain.ast import ExprAst, NumberExprAst


class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self._lexer: Lexer = lexer
        self._current_token: Optional[Token] = None

    def parse(self) -> None:
        pass

    def empty_expression(reason: str) -> None:
        print(reason, file=sys.stderr)
        return None

    def get_next_token(self) -> None:
        self._current_token = self._lexer.try_get_next_token()

    # number
    def parse_number_expression(self) -> ExprAst:
        assert self._current_token
        assert self._current_token.value

        expr = NumberExprAst(value=float(self._current_token.value()))

        # Consume number and move to next token
        self.get_next_token()

        return expr

    # '(' expression ')'
    def parse_parentheses_expression(self) -> Optional[ExprAst]:
        self.get_next_token()  # eat (

        v: Optional[Any] = self.parse_expression()

        if not v:
            return None

        if self._current_token.value() != ")":
            return self.empty_expression(reason="expected ')'")

        self.get_next_token()  # eat )

        return v
