from enum import Enum, auto
from typing import MutableSequence, Optional


class NodeType(Enum):
    ATOM = auto()
    FUNCTION_DEF = auto()
    RETURN_STATEMENT = auto()
    SUM = auto()
    ASSIGNMENT = auto()
    FUNCTION_CALL = auto()
    PARAMETER = auto()


class Node:
    Type = NodeType

    def __init__(self, node_type: NodeType, name: Optional[str] = None):
        self._node_type: NodeType = node_type
        self._name: Optional[str] = name

    def name(self) -> str:
        return self._name if self._name else ""

    def set_name(self, name: str) -> "Node":
        self._name: str = name
        return self

    def node_type(self) -> NodeType:
        return self._node_type

    def set_node_type(self, node_type: NodeType) -> "Node":
        self._node_type: NodeType = node_type
        return self

    def is_complete(self) -> bool:
        raise NotImplementedError()

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"type = '{self.node_type().name}', "
            f"name = '{self.name()}'"
            f")"
        )


class Atom(Node):
    def __init__(self):
        super().__init__(node_type=Node.Type.ATOM)

    def is_complete(self) -> bool:
        return self.name() is not None


class DataTypeName(Enum):
    NONE = auto()
    BOOL = auto()
    INT = auto()
    FLOAT = auto()
    STR = auto()


class DataType:
    Name = DataTypeName

    def __init__(self, name: DataTypeName):
        self._name: DataTypeName = name

    def name(self) -> DataTypeName:
        return self._name

    @classmethod
    def none_type(cls) -> "DataType":
        return DataType(name=DataTypeName.NONE)


class Expression(Node):
    def __init__(self, node_type: Node.Type):
        super().__init__(node_type=node_type)


class Parameter(Node):
    def __init__(self):
        super().__init__(node_type=Node.Type.PARAMETER)
        self._data_type: Optional[DataType] = None
        self._default_value: Optional[Expression] = None

    def data_type(self) -> DataType:
        if self._data_type is None:
            return DataType.none_type()

        return self._data_type

    def set_data_type(self, data_type: DataType) -> "Parameter":
        self._data_type: DataType = data_type
        return self

    def default_value(self) -> Optional[Expression]:
        return self._default_value

    def set_default_value(self, default_value: Optional[Expression]) -> "Parameter":
        self._default_value: Optional[Expression] = default_value
        return self

    def is_complete(self) -> bool:
        return self._data_type is not None


class Sum(Expression):
    def __init__(self):
        super().__init__(node_type=Node.Type.SUM)
        self._left: Optional[Expression] = None
        self._right: Optional[Expression] = None

    def left(self) -> Optional[Expression]:
        return self._left

    def set_left(self, left: Expression) -> "Sum":
        self._left = left
        return self

    def right(self) -> Optional[Expression]:
        return self._right

    def set_right(self, right: Expression) -> "Sum":
        self._right = right
        return self

    def is_complete(self) -> bool:
        return self.left() is not None and self.right() is not None


class Statement(Node):
    def __init__(self, node_type: Node.Type):
        super().__init__(node_type=node_type)


class Return(Statement):
    def __init__(self):
        super().__init__(node_type=Node.Type.RETURN_STATEMENT)
        self._expressions: MutableSequence[Expression] = []

    def return_type(self) -> DataType:
        # Calculate this from the expressions
        pass

    def expressions(self) -> MutableSequence[Expression]:
        return self._expressions

    def is_complete(self) -> bool:
        # Return statements can always return nothing, which defaults to None
        return True


class FunctionDef(Statement):
    def __init__(self):
        super().__init__(node_type=Node.Type.FUNCTION_DEF)
        self._parameters: MutableSequence[Parameter] = []
        self._statements: MutableSequence[Statement] = []
        self._return_type: Optional[DataType] = None

    def parameters(self) -> MutableSequence[Parameter]:
        return self._parameters

    def statements(self) -> MutableSequence[Statement]:
        return self._statements

    def return_type(self) -> DataType:
        if self._return_type is not None:
            return self._return_type

        return DataType(name=DataTypeName.NONE)

    def set_return_type(self, return_type: DataType) -> "FunctionDef":
        self._return_type: DataType = return_type
        return self

    def is_complete(self) -> bool:
        return self.name() is not None and self._return_type is not None


class Argument(Expression):
    def __init__(self, node_type: Node.Type):
        super().__init__(node_type=node_type)


class FunctionCall(Statement):
    def __init__(self):
        super().__init__(node_type=Node.Type.FUNCTION_CALL)
        self._arguments: MutableSequence[Argument] = []

    def arguments(self) -> MutableSequence[Argument]:
        return self._arguments

    def return_type(self) -> DataType:
        # Calculate from function call
        pass

    def is_complete(self) -> bool:
        # Function call doesn't need arguments, but does need a name
        # TODO: or maybe an expression...
        return self.name() is not None


class Variable(Node):
    def __init__(self):
        super().__init__(node_type=Node.Type.VARIABLE)


class Assignment(Statement):
    def __init__(self):
        super().__init__(node_type=Node.Type.ASSIGNMENT)
        self._left: Optional[Variable] = None
        self._right: Optional[Expression] = None

    def left(self) -> Optional[Expression]:
        return self._left

    def set_left(self, left: Variable) -> "Sum":
        self._left = left
        return self

    def right(self) -> Optional[Expression]:
        return self._right

    def set_right(self, right: Expression) -> "Sum":
        self._right = right
        return self

    def is_complete(self) -> bool:
        return self.left() is not None and self.right() is not None
