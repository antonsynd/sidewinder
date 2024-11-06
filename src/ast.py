from typing import Sequence
import sys

from lexer import Lexer, Token
from typing import Any, Optional


class ExprAst:
    pass


class NumberExprAst(ExprAst):
    def __init__(self, val: float) -> None:
        super().__init__()

        self._val: float = val


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

    def log_error(s: str) -> None:
        print(s, file=sys.stderr)
        return None

    def get_next_token(self) -> None:
        self._current_token = self._lexer.try_get_next_token()

    def parse_number_expression(self) -> ExprAst:
        expr = NumberExprAst(val=self._lexer._num_val)

        # Consume number and move to next token
        self.get_next_token()

        return expr

    def parse_parentheses_expression(self) -> Optional[ExprAst]:
        self.get_next_token()  # eat (

        v: Optional[Any] = self.parse_expression()

        if not v:
            return None

        # if current_token !=
