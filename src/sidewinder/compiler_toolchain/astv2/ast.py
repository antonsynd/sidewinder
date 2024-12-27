from typing import MutableSequence, Union


class AST:
    pass


class Statement(AST):
    def __init__(self):
        super().__init__()


class Module(AST):
    def __init__(self):
        super().__init__()

        self.body: MutableSequence[Statement] = []


class FunctionType(AST):
    def __init__(self):
        super().__init__()

        self.argtypes: MutableSequence[Expression] = []
        self.returns: Expression


class Constant(AST):
    def __init__(self):
        super().__init__()

        self.value: str


class FormattedValue(AST):
    """
    Single formatting field in an f-string
    """

    def __init__(self):
        super().__init__()

        self.value: Expression
        self.conversion: int
        self.format_spec: JoinedStr


class JoinedStr(AST):
    """
    An f-string
    """

    def __init__(self):
        super().__init__()

        self.values: MutableSequence[Union[FormattedValue, Constant]]


class List(AST):
    def __init__(self):
        super().__init__()

        self.elts: MutableSequence[AST] = []
        # Store if assignment target, else Load
        self.ctx: Union[Store, Load]


class Tuple(AST):
    def __init__(self):
        super().__init__()

        self.elts: MutableSequence[AST] = []
        # Store if assignment target, else Load
        self.ctx: Union[Store, Load]


class Set(AST):
    def __init__(self):
        super().__init__()

        self.elts: MutableSequence[AST] = []


class Dict(AST):
    def __init__(self):
        super().__init__()

        # Unpacking puts the expression into values and None at keys
        self.keys: MutableSequence[AST] = []
        self.values: MutableSequence[AST] = []


class Name(AST):
    def __init__(self):
        super().__init__()

        self.id: str
        self.ctx: Union[Load, Store, Del]


class Load(AST):
    def __init__(self):
        super().__init__()


class Store(AST):
    def __init__(self):
        super().__init__()


class Del(AST):
    def __init__(self):
        super().__init__()


class Starred(AST):
    def __init__(self):
        super().__init__()

        self.value: Name
        self.ctx: Store


class Expression(AST):
    def __init__(self):
        super().__init__()


class Expr(Expression):
    def __init__(self):
        super().__init__()
        self.value: Union[Constant, Name, Lambda, Yield, YieldFrom]


class UnaryOp(Expression):
    def __init__(self):
        super().__init__()

        self.op: Union[UAdd, USub, Not, Invert]
        self.operand: Expression


class UAdd(AST):
    def __init__(self):
        super().__init__()


class USub(AST):
    def __init__(self):
        super().__init__()


class Not(AST):
    def __init__(self):
        super().__init__()


class Invert(AST):
    def __init__(self):
        super().__init__()


class BinOp(AST):
    def __init__(self):
        super().__init__()

        self.left: Expression
        self.op = Union[
            Add, Sub, Mult, Div, FloorDiv, Mod, Pow, LShift, RShift, BitOr, BitXor, BitAnd, MatMult
        ]
        self.right: Expression


class Add(AST):
    def __init__(self):
        super().__init__()


class Sub(AST):
    def __init__(self):
        super().__init__()


class Mult(AST):
    def __init__(self):
        super().__init__()


class Div(AST):
    def __init__(self):
        super().__init__()


class FloorDiv(AST):
    def __init__(self):
        super().__init__()


class Mod(AST):
    def __init__(self):
        super().__init__()


class Pow(AST):
    def __init__(self):
        super().__init__()


class LShift(AST):
    def __init__(self):
        super().__init__()


class RShift(AST):
    def __init__(self):
        super().__init__()


class BitOr(AST):
    def __init__(self):
        super().__init__()


class BitXor(AST):
    def __init__(self):
        super().__init__()


class BitAnd(AST):
    def __init__(self):
        super().__init__()


class MatMult(AST):
    def __init__(self):
        super().__init__()


class BoolOp(Expression):
    def __init__(self):
        super().__init__()

        self.op: Union[Or, And]
        self.values: MutableSequence[Expression]


class Or(AST):
    def __init__(self):
        super().__init__()


class And(AST):
    def __init__(self):
        super().__init__()


class Compare(Expression):
    def __init__(self):
        super().__init__()

        self.left: Expression
        self.ops: MutableSequence[Union[Eq, NotEq, Lt, LtE, Gt, GtE, Is, IsNot, In, NotIn]] = []
        self.comparators: MutableSequence[Expression]


class Eq(AST):
    def __init__(self):
        super().__init__()


class NotEq(AST):
    def __init__(self):
        super().__init__()


class Lt(AST):
    def __init__(self):
        super().__init__()


class LtE(AST):
    def __init__(self):
        super().__init__()


class Gt(AST):
    def __init__(self):
        super().__init__()


class GtE(AST):
    def __init__(self):
        super().__init__()


class Is(AST):
    def __init__(self):
        super().__init__()


class IsNot(AST):
    def __init__(self):
        super().__init__()


class In(AST):
    def __init__(self):
        super().__init__()


class NotIn(AST):
    def __init__(self):
        super().__init__()


class Call(Expression):
    def __init__(self):
        super().__init__()

        self.func: Union[Name, Attribute]
        self.args: MutableSequence[Expression] = []
        self.keywords: MutableSequence[keyword] = []


class keyword(AST):
    def __init__(self):
        super().__init__()

        self.arg: str
        self.value: Expression


class IfExp(Expression):
    def __init__(self):
        super().__init__()

        self.test: Expression
        self.body: Expression
        self.orelse: Expression


class Attribute(Expression):
    def __init__(self):
        super().__init__()

        self.value: Name
        self.attr: str
        self.ctx: Union[Load, Store, Del]


class NamedExpr(Expression):
    """
    if (n := "str"):
        print(n)
    """

    def __init__(self):
        super().__init__()

        self.target: Name
        self.value: Expression
