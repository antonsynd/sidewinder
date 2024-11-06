from typing import Sequence


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
