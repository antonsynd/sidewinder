from typing import Sequence


class ExprAST:
    pass


class NumberExprAST(ExprAST):
    def __init__(self, value: float) -> None:
        super().__init__()

        self._value: float = value

    def __str__(self) -> str:
        return f"NumberExprAST(value = {self._value})"


class VariableExprAST(ExprAST):
    def __init__(self, name: str) -> None:
        super().__init__()

        self._name: str = name

    def __str__(self) -> str:
        return f"VariableExprAST(name = {self._name})"


class BinaryExprAST(ExprAST):
    def __init__(self, op: str, lhs: ExprAST, rhs: ExprAST) -> None:
        super().__init__()

        self._op: str = op
        self._lhs: ExprAST = lhs
        self._rhs: ExprAST = rhs

    def __str__(self) -> str:
        return f"BinaryExprAST(op = '{self._op}', lhs = {self._lhs}, rhs = {self._rhs})"


class CallExprAST(ExprAST):
    def __init__(self, callee: str, args: Sequence[ExprAST]) -> None:
        super().__init__()

        self._callee: str = callee
        self._args: Sequence[ExprAST] = args

    def __str__(self) -> str:
        args_str: str = ", ".join([str(x) for x in self._args])
        return f"CallExprAST(callee = '{self._callee}', args = [{args_str}])"


class PrototypeAST:
    def __init__(self, name: str, args: Sequence[str]) -> None:
        self._name: str = name
        self._args: Sequence[str] = args

    def get_name(self) -> str:
        return self._name

    def __str__(self) -> str:
        args_str: str = ", ".join(self._args)
        return f"PrototypeAST(name = '{self._name}', args = [{args_str}])"


class FunctionAST:
    # TODO: add return type and type of arguments
    def __init__(self, proto: PrototypeAST, body: ExprAST) -> None:
        self._proto: PrototypeAST = proto
        self._body: ExprAST = body

    def __str__(self) -> str:
        return f"FunctionAST(proto = {self._proto}, body = {self._body})"
