from typing import Sequence
from typing import Any, Optional
import sys

from sidewinder.lexer import Lexer
from sidewinder.token import Token


class ExprAst:
    pass


class NumberExprAst(ExprAst):
    def __init__(self, value: float) -> None:
        super().__init__()

        self._value: float = value


class VariableExprAst(ExprAst):
    def __init__(self, name: str) -> None:
        super().__init__()

        self._name: str = name


class BinaryExprAst(ExprAst):
    def __init__(self, op: str, lhs: ExprAst, rhs: ExprAst) -> None:
        super().__init__()

        self._op: str = op
        self._lhs: ExprAst = lhs
        self._rhs: ExprAst = rhs


class CallExprAst(ExprAst):
    def __init__(self, callee: str, args: Sequence[ExprAst]) -> None:
        super().__init__()

        self._callee: str = callee
        self._args: Sequence[ExprAst] = args


class PrototypeAst:
    def __init__(self, name: str, args: Sequence[str]) -> None:
        self._name: str = name
        self._args: Sequence[str] = args

    def get_name(self) -> str:
        return self._name


class FunctionAst:
    # TODO: add return type and type of arguments
    def __init__(self, proto: PrototypeAst, body: ExprAst) -> None:
        self._proto: PrototypeAst = proto
        self._body: ExprAst = body


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
