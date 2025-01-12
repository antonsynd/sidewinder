from typing import MutableSequence, Type, Union, Tuple, Dict, AbstractSet, Optional, Sequence
from enum import Enum, auto
from io import StringIO


class Source:
    """
    Container for the source of a particular AST node.
    """

    def __init__(
        self, lineno: int = -1, col_offset: int = -1, end_lineno: int = -1, end_col_offset: int = -1
    ):
        self.lineno: int = lineno
        self.col_offset: int = col_offset
        self.end_lineno: int = end_lineno
        self.end_col_offset: int = end_col_offset

    def __repr__(self) -> str:
        buffer = StringIO()
        buffer.write("Source(")

        properties: Sequence[str] = [
            f"lineno = {self.lineno}"
            f"col_offset = {self.col_offset}"
            f"end_lineno = {self.end_lineno}"
            f"end_col_offset = {self.end_col_offset}"
        ]

        buffer.write(", ".join(properties))
        buffer.write(")")

        return buffer.getvalue()


class AST:
    """
    Base class for all AST nodes.
    """

    def __init__(self, source: Optional[Source] = None):
        self.source: Optional[Source] = source

    def __repr__(self) -> str:
        buffer = StringIO()
        buffer.write("AST(")

        properties: Sequence[str] = [f"source = {self.source}"]

        buffer.write(", ".join(properties))
        buffer.write(")")

        return buffer.getvalue()


class Module(AST):
    """
    Contains the code for a module (a file).
    """

    def __init__(self, body: MutableSequence[AST]):
        super().__init__()

        self.body: MutableSequence[AST] = body

    def __repr__(self) -> str:
        buffer = StringIO()
        buffer.write("Module(")

        properties: Sequence[str] = [
            f"source = {self.source}",
            f"body = {self.body}",
        ]

        buffer.write(", ".join(properties))
        buffer.write(")")

        return buffer.getvalue()


class FunctionType(AST):
    """
    TODO: should be function signature to include the argument names.
    """

    def __init__(self, argtypes: MutableSequence[AST], returns: Optional[AST] = None):
        super().__init__()

        self.argtypes: MutableSequence[AST] = argtypes
        self.returns: Optional[AST] = returns

    def __repr__(self) -> str:
        buffer = StringIO()
        buffer.write("FunctionType(")

        properties: Sequence[str] = [
            f"source = {self.source}",
            f"argtypes = {self.argtypes}",
            f"returns = {self.returns}",
        ]

        buffer.write(", ".join(properties))
        buffer.write(")")

        return buffer.getvalue()


class ConstantType(Enum):
    BIG_INT = "bigint"
    BYTE = "byte"
    BYTES = "bytes"
    COMPLEX = "complex"
    DOUBLE = "double"
    ELLIPSIS = "Ellipsis"  # Maybe ... ?
    FLOAT = "float"
    INT = "int"
    NONE = "None"
    STR = "str"


class Constant(AST):
    """
    Any literal.
    """

    def __init__(self, value: str, kind: ConstantType):
        super().__init__()

        self.value: str = value
        self.kind: ConstantType = kind

    def __repr__(self) -> str:
        buffer = StringIO()
        buffer.write("Constant(")

        properties: Sequence[str] = [
            f"source = {self.source}",
            f"value = {self.value}",
            f"kind = {self.kind}",
        ]

        buffer.write(", ".join(properties))
        buffer.write(")")

        return buffer.getvalue()


class FormattedValue(AST):
    """
    Single formatting field in an f-string

    {:0f}
    """

    def __init__(self):
        super().__init__()

        self.value: AST
        self.conversion: int
        self.format_spec: AST


class JoinedStr(AST):
    """
    An f-string.

    f"foobar"
    """

    def __init__(self):
        super().__init__()

        self.values: MutableSequence[Union[FormattedValue, Constant]]


class List(AST):
    """
    A list literal.

    [a, b] = [1, 3]  # store (assignment target)
    a = [1, 3]       # load
    """

    def __init__(self):
        super().__init__()

        self.elts: MutableSequence[AST] = []
        # Store if assignment target, else Load
        self.ctx: Union[Store, Load]


class Tuple(AST):
    """
    A tuple literal.

    (a, b) = [1, 3]  # store (assignment target)
    a = (1, 3)       # load
    """

    def __init__(self):
        super().__init__()

        self.elts: MutableSequence[AST] = []
        # Store if assignment target, else Load
        self.ctx: Union[Store, Load]


class Set(AST):
    """
    A set literal.
    """

    def __init__(self):
        super().__init__()

        self.elts: MutableSequence[AST] = []


class Dict(AST):
    """
    A dict literal.
    """

    def __init__(self):
        super().__init__()

        # Unpacking puts the AST into values and None at keys
        # {"a": 5, *other}
        # keys = {"a", None}
        # values = {5, values of other}
        self.keys: MutableSequence[AST] = []
        self.values: MutableSequence[AST] = []


class Context(AST):
    def __init__(self):
        super().__init__()


class Name(AST):
    """
    Any identifier.
    """

    def __init__(self):
        super().__init__()

        self.id: str
        self.ctx: Context


class Load(Context):
    """
    Context where a name is loaded (accessed).

    ... = name
    """

    def __init__(self):
        super().__init__()


class Store(Context):
    """
    Context where a name is the target for storing a value (setting).

    name = ...
    """

    def __init__(self):
        super().__init__()


class Del(Context):
    """
    Context where a name is the target for deletion.

    del name
    """

    def __init__(self):
        super().__init__()


class Starred(AST):
    def __init__(self, value: Name):
        super().__init__()

        self.value: Name
        self.ctx: Context = Store()


class Expr(AST):
    def __init__(self):
        super().__init__()
        self.value: Union[Constant, Name, Lambda, Yield, YieldFrom]


class UnaryOp(AST):
    def __init__(self):
        super().__init__()

        self.op: Union[UAdd, USub, Not, Invert]
        self.operand: AST


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

        self.left: AST
        self.op = Union[
            Add, Sub, Mult, Div, FloorDiv, Mod, Pow, LShift, RShift, BitOr, BitXor, BitAnd, MatMult
        ]
        self.right: AST


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


class BoolOp(AST):
    def __init__(self):
        super().__init__()

        self.op: Union[Or, And]
        self.values: MutableSequence[AST]


class Or(AST):
    def __init__(self):
        super().__init__()


class And(AST):
    def __init__(self):
        super().__init__()


class Compare(AST):
    def __init__(self):
        super().__init__()

        self.left: AST
        self.ops: MutableSequence[Union[Eq, NotEq, Lt, LtE, Gt, GtE, Is, IsNot, In, NotIn]] = []
        self.comparators: MutableSequence[AST]


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


class Call(AST):
    def __init__(self):
        super().__init__()

        self.func: Union[Name, Attribute]
        self.args: MutableSequence[AST] = []
        self.keywords: MutableSequence[keyword] = []


class keyword(AST):
    def __init__(self):
        super().__init__()

        self.arg: str
        self.value: AST


class IfExp(AST):
    def __init__(self):
        super().__init__()

        self.test: AST
        self.body: AST
        self.orelse: AST


class Attribute(AST):
    def __init__(self):
        super().__init__()

        self.value: Name
        self.attr: str
        self.ctx: Union[Load, Store, Del]


class NamedExpr(AST):
    """
    if (n := "str"):
        print(n)
    """

    def __init__(self):
        super().__init__()

        self.target: Name
        self.value: AST


class Subscript(AST):
    def __init__(self):
        super().__init__()

        self.value: AST
        self.slice: slice
        self.ctx: Union[Load, Store, Del]


class Slice(AST):
    def __init__(self):
        super().__init__()

        self.lower: int
        self.upper: int
        self.step: int


class Comprehension:
    def __init__(self, target: AST, iter: AST, ifs: MutableSequence[AST], is_async: bool):
        self.target: AST = target
        self.iter: AST = iter
        self.ifs: MutableSequence[AST] = ifs
        self.is_async: bool = is_async


class CompBase(AST):
    def __init__(self, elt: AST, generators: MutableSequence[Comprehension]):
        super().__init__()

        self.elt: AST = elt
        self.generators: MutableSequence[Comprehension] = generators


class ListComp(CompBase):
    def __init__(self, elt: AST, generators: MutableSequence[Comprehension]):
        super().__init__(elt, generators)


class SetComp(CompBase):
    def __init__(self, elt: AST, generators: MutableSequence[Comprehension]):
        super().__init__(elt, generators)


class GeneratorExp(CompBase):
    def __init__(self, elt: AST, generators: MutableSequence[Comprehension]):
        super().__init__(elt, generators)


class DictComp(AST):
    def __init__(self, key: AST, value: AST, generators: MutableSequence[Comprehension]):
        super().__init__()

        self.key: AST = key
        self.value: AST = value
        self.generators: MutableSequence[Comprehension] = generators


Assignable = Union[Name, Tuple, List]


class Assign(AST):
    # a = b = 1
    # (a, b) = (2, 3)
    # e = (a, b) = [c, d] = (4, 5)
    def __init__(self, targets: MutableSequence[Assignable], value: AST):
        super().__init__()

        self.targets: MutableSequence[Assignable] = targets
        self.value: AST = value


class AnnAssign(AST):
    # Annotated assignment
    def __init__(self, target: AST, annotation: AST, value: Optional[AST], simple: bool):
        super().__init__()

        self.target: AST = target
        self.annotation: AST = annotation
        self.value: Optional[AST] = value
        self.simple: bool = simple


class Operator(Enum):
    PLUS = "+"
    MINUS = "-"


class AugAssign(AST):
    def __init__(self, target: AST, op: Operator, value: AST):
        super().__init__()

        self.target: AST = target
        self.op: Operator = op
        self.value: AST = value


class Raise(AST):
    # raise x
    # raise x from y
    def __init__(self, exc: Optional[AST], cause: Optional[AST]):
        super().__init__()

        self.exc: Optional[AST] = exc
        self.cause: Optional[AST] = cause


class Assert(AST):
    # assert x, "message"
    def __init__(self, test: AST, msg: Optional[AST]):
        super().__init__()

        self.test: AST = test
        self.msg: Optional[AST] = msg


class Delete(AST):
    # del x, y, z
    def __init__(self, targets: MutableSequence[AST]):
        super().__init__()

        self.targets: MutableSequence[AST] = targets


class Pass(AST):
    # pass
    def __init__(self):
        super().__init__()


class TypeAlias(AST):
    def __init__(self, name: AST, type_params: MutableSequence[AST], value: AST):
        super().__init__()

        self.name: AST
        self.type_params: MutableSequence[AST] = type_params
        self.value: AST = value


class Alias(AST):
    def __init__(self, name: str, asname: Optional[str]):
        super().__init__()

        self.name: str = name
        self.asname: Optional[str] = asname


class Import(AST):
    def __init__(self, names: MutableSequence[Alias]):
        super().__init__()

        self.names: MutableSequence[Alias] = names


class ImportFrom(AST):
    def __init__(self, module: Optional[str], names: MutableSequence[Alias], level: Optional[int]):
        super().__init__()

        self.module: Optional[str] = module
        self.names: MutableSequence[Alias] = names
        self.level: Optional[int] = level


class If(AST):
    def __init__(self, test: AST, body: AST, orelse: MutableSequence[AST]):
        super().__init__()

        self.test: AST = test
        self.body: AST = body
        self.orelse: MutableSequence[AST] = orelse


class For(AST):
    def __init__(
        self, target: AST, iter: AST, body: MutableSequence[AST], orelse: MutableSequence[AST]
    ):
        super().__init__()

        self.target: AST = target
        self.iter: AST = iter
        self.body: MutableSequence[AST] = body
        self.orelse: MutableSequence[AST] = orelse


class While(AST):
    def __init__(self, test: AST, body: AST, orelse: MutableSequence[AST]):
        super().__init__()

        self.test: AST = test
        self.body: AST = body
        self.orelse: MutableSequence[AST] = orelse


class Break(AST):
    def __init__(self):
        super().__init__()


class Continue(AST):
    def __init__(self):
        super().__init__()


class ExceptHandler(AST):
    """
    type: None if there's no exception type provided

    except type as name:
        body
    """

    def __init__(self, type: Optional[Name], name: Optional[str], body: MutableSequence[AST]):
        super().__init__()

        self.type: Optional[Name] = type
        self.name: Optional[str] = name
        self.body: MutableSequence[AST] = body


class Try(AST):
    def __init__(
        self,
        body: MutableSequence[AST],
        handlers: MutableSequence[ExceptHandler],
        orelse: MutableSequence[AST],
        finalbody: MutableSequence[AST],
    ):
        super().__init__()

        self.body: MutableSequence[AST] = body
        self.handlers: MutableSequence[ExceptHandler] = handlers
        self.orelse: MutableSequence[AST] = orelse
        self.finalbody: MutableSequence[AST] = finalbody


class TryStar(Try):
    def __init__(
        self,
        body: MutableSequence[AST],
        handlers: MutableSequence[ExceptHandler],
        orelse: MutableSequence[AST],
        finalbody: MutableSequence[AST],
    ):
        super().__init__(body=body, handlers=handlers, orelse=orelse, finalbody=finalbody)


class withitem(AST):
    def __init__(
        self,
        context_expr: Union[AST, Name, Call],
        optional_vars: Optional[Union[Name, Tuple, List]],
    ):
        super().__init__()

        self.context_expr: Union[AST, Name, Call] = context_expr
        self.optional_vars: Optional[Union[Name, Tuple, List]] = optional_vars


class With(AST):
    def __init__(self, items: MutableSequence[withitem], body: MutableSequence[AST]):
        super().__init__()

        self.items: MutableSequence[withitem] = items
        self.body: MutableSequence[AST] = body


class match_case(AST):
    def __init__(self, pattern: AST, guard: Optional[AST], body: MutableSequence[AST]):
        super().__init__()

        self.pattern: AST = pattern
        self.guard: Optional[AST] = guard
        self.body: MutableSequence[AST] = body


class Match(AST):
    def __init__(self, subject: AST, cases: MutableSequence[match_case]):
        super().__init__()

        self.subject: AST = subject
        self.cases: MutableSequence[match_case] = cases


class MatchValue(AST):
    def __init__(self, value: Constant):
        super().__init__()

        self.value: Constant = value


class MatchSingleton(AST):
    """
    match x:
        case None:
            pass

    value = None
    """

    def __init__(self, value: Constant):
        super().__init__()

        # according to the docs, this should only
        # be True, False, or None. Use MatchValue
        # otherwise.
        self.value: Constant = value


class MatchSequence(AST):
    """
    match x:
        case [1, 2]:
            pass

    patterns = [1, 2]
    """

    def __init__(self, patterns: MutableSequence[MatchValue]):
        super().__init__()

        self.patterns: MutableSequence[MatchValue] = patterns


class MatchStar(AST):
    """
    match x:
        case [1, 2, *rest]:
            pass
        case [*_]:
            pass

    name = rest or None
    """

    def __init__(self, name: Optional[str]):
        super().__init__()

        self.name: Optional[str] = name


class MatchMapping(AST):
    """
    match x:
        case {1: _, 2: _}:
            pass
        case {**rest}:
            pass

    keys = [1, 2], patterns = [MatchAs(), MatchAs()]
    rest = rest
    """

    def __init__(
        self, keys: MutableSequence[AST], patterns: MutableSequence[AST], rest: Optional[Name]
    ):
        super().__init__()

        self.keys: MutableSequence[AST] = keys
        self.patterns: MutableSequence[AST] = patterns
        self.rest: Optional[Name] = rest


class MatchClass(AST):
    """
    match x:
        case Point2D(0, 0)
            pass
        case Point3D(x=0, y=0, z=0)
            pass
    """

    def __init__(
        self,
        cls: AST,
        patterns: MutableSequence[AST],
        kwd_attrs: MutableSequence[str],
        kwd_patterns: MutableSequence[MatchValue],
    ):
        super().__init__()

        self.cls: AST = cls
        self.patterns: MutableSequence[AST] = patterns
        self.kwd_attrs: MutableSequence[str] = kwd_attrs
        self.kwd_patters: MutableSequence[MatchValue] = kwd_patterns


class MatchAs(AST):
    """
    match x:
        case [x] as y:
            pass
        case _
            pass

    pattern = MatchSequence(x), name = y
    pattern = None, name = None
    """

    def __init__(self, pattern: Optional[AST], name: Optional[str]):
        super().__init__()

        self.pattern: Optional[AST] = pattern
        self.name: Optional[str] = name


class MatchOr(AST):
    """
    match x:
        case [x] | (y):
            pass
    """

    def __init__(self, patterns: MutableSequence[AST]):
        super().__init__()

        self.patterns: MutableSequence[AST] = patterns


class TypeVar(AST):
    """
    type Alias[T: int = bool] = List[T]

    name = Alias, bound = int, default_value = bool

    bound = T must be a subtype
    default_value = T is this if not specified
    """

    def __init__(
        self, name: str, bound: Optional[Union[Tuple, Name]], default_value: Optional[Name]
    ):
        super().__init__()

        self.name: str = name
        self.bound: Optional[Union[Tuple, Name]] = bound
        self.default_value: Optional[Name] = default_value


class ParamSpec(AST):
    """
    type Alias[**P = [int, str]] = Callable[P, int]
    """

    def __init__(self, name: str, default_value: Optional[AST]):
        super().__init__()

        self.name: str = name
        self.default_value: Optional[AST] = default_value


class TypeVarTuple(AST):
    """
    type Alias[*Ts = ()] = tuple[*Ts]
    """

    def __init__(self, name: str, default_value: Optional[AST]):
        super().__init__()

        self.name: str = name
        self.default_value: Optional[AST] = default_value


class arguments(AST):
    def __init__(self, posonlyargs, args, vararg, kwonlyargs, kw_defaults, kwarg, defaults):
        super().__init__()


class arg(AST):
    def __init__(self, arg, annotation, type_comment):
        super().__init__()


class FunctionDef(AST):
    def __init__(
        self,
        name: str,
        args: arguments,
        body: MutableSequence[AST],
        decorator_list: MutableSequence[AST],
        returns: AST,
        type_params: MutableSequence[AST],
    ):
        super().__init__()

        self.name: str = name
        self.args: arguments = args
        self.body: MutableSequence[AST] = body
        self.decorator_list: MutableSequence[AST] = decorator_list
        self.returns: AST = returns
        self.type_params: MutableSequence[AST] = type_params


class Lambda(AST):
    def __init__(self, args: arguments, body: MutableSequence[AST]):
        super().__init__()

        self.args: arguments = args
        self.body: MutableSequence[AST] = body


class Return(AST):
    def __init__(self, value: Optional[AST]):
        super().__init__()

        self.value: Optional[AST] = value


class Yield(AST):
    def __init__(self, value: AST):
        super().__init__()

        self.value: AST = value


class YieldFrom(AST):
    def __init__(self, value: AST):
        super().__init__()

        self.value: AST = value


class Global(AST):
    def __init__(self, names: MutableSequence[str]):
        super().__init__()

        self.names: MutableSequence[str] = names


class Nonlocal(AST):
    def __init__(self, names: MutableSequence[str]):
        super().__init__()

        self.names: MutableSequence[str] = names


class ClassDef(AST):
    def __init__(
        self,
        name: str,
        bases: MutableSequence[Name],
        keywords: MutableSequence[keyword],
        body: MutableSequence[AST],
        decorator_list: MutableSequence[AST],
        type_params: MutableSequence[AST],
    ):
        super().__init__()

        self.name: str = name
        self.bases: MutableSequence[Name] = bases
        self.keywords: MutableSequence[keyword] = keywords
        self.body: MutableSequence[AST] = body
        self.decorator_list: MutableSequence[AST] = decorator_list
        self.type_params: MutableSequence[AST] = type_params


class AsyncFunctionDef(AST):
    def __init__(
        self,
        name: str,
        args: arguments,
        body: MutableSequence[AST],
        decorator_list: MutableSequence[AST],
        returns: AST,
        type_params: MutableSequence[AST],
    ):
        super().__init__()

        self.name: str = name
        self.args: arguments = args
        self.body: MutableSequence[AST] = body
        self.decorator_list: MutableSequence[AST] = decorator_list
        self.returns: AST = returns
        self.type_params: MutableSequence[AST] = type_params


class Await(AST):
    def __init__(self, value: AST):
        super().__init__()

        self.value: AST = value


class AsyncFor(AST):
    def __init__(
        self, target: AST, iter: AST, body: MutableSequence[AST], orelse: MutableSequence[AST]
    ):
        super().__init__()

        self.target: AST = target
        self.iter: AST = iter
        self.body: MutableSequence[AST] = body
        self.orelse: MutableSequence[AST] = orelse


class AsyncWith(AST):
    def __init__(self, items: MutableSequence[withitem], body: MutableSequence[AST]):
        super().__init__()

        self.items: MutableSequence[withitem] = items
        self.body: MutableSequence[AST] = body
