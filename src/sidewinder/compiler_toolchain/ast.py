from typing import Sequence


class ExprAst:
    pass


class NumberExprAst(ExprAst):
    def __init__(self, value: float) -> None:
        super().__init__()

        self._value: float = value

    def __str__(self) -> str:
        return f"NumberExprAst(value = {self._value})"


class VariableExprAst(ExprAst):
    def __init__(self, name: str) -> None:
        super().__init__()

        self._name: str = name

    def __str__(self) -> str:
        return f"VariableExprAst(name = {self._name})"


class BinaryExprAst(ExprAst):
    def __init__(self, op: str, lhs: ExprAst, rhs: ExprAst) -> None:
        super().__init__()

        self._op: str = op
        self._lhs: ExprAst = lhs
        self._rhs: ExprAst = rhs

    def __str__(self) -> str:
        return f"BinaryExprAst(op = '{self._op}', lhs = {self._lhs}, rhs = {self._rhs})"


class CallExprAst(ExprAst):
    def __init__(self, callee: str, args: Sequence[ExprAst]) -> None:
        super().__init__()

        self._callee: str = callee
        self._args: Sequence[ExprAst] = args

    def __str__(self) -> str:
        args_str: str = ", ".join([str(x) for x in self._args])
        return f"CallExprAst(callee = '{self._callee}', args = [{args_str}])"


class PrototypeAst:
    def __init__(self, name: str, args: Sequence[str]) -> None:
        self._name: str = name
        self._args: Sequence[str] = args

    def get_name(self) -> str:
        return self._name

    def __str__(self) -> str:
        args_str: str = ", ".join(self._args)
        return f"PrototypeAst(name = '{self._name}', args = [{args_str}])"


class FunctionAst:
    # TODO: add return type and type of arguments
    def __init__(self, proto: PrototypeAst, body: ExprAst) -> None:
        self._proto: PrototypeAst = proto
        self._body: ExprAst = body

    def __str__(self) -> str:
        return f"FunctionAst(proto = {self._proto}, body = {self._body})"
