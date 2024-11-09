from enum import Enum, auto
from typing import MutableSequence, Optional


class ASTNodeType(Enum):
    ATOM = auto()
    FUNCTION_DEF = auto()
    RETURN_STATEMENT = auto()
    SUM = auto()
    ASSIGNMENT = auto()
    FUNCTION_CALL = auto()


class ASTNode:
    Type = ASTNodeType

    def __init__(self, node_type: ASTNodeType, name: Optional[str] = None):
        self._node_type: ASTNodeType = node_type
        self._name: Optional[str] = name

    def name(self) -> str:
        return self._name if self._name else ""

    def set_name(self, name: str) -> None:
        self._name: str = name

    def node_type(self) -> ASTNodeType:
        return self._node_type

    def set_node_type(self, node_type: ASTNodeType) -> None:
        self._node_type: ASTNodeType = node_type

    def is_complete(self) -> bool:
        raise NotImplementedError()

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"type = '{self.node_type().name}', "
            f"name = '{self.name()}'"
            f")"
        )


class AtomASTNode(ASTNode):
    def __init__(self):
        super().__init__(node_type=ASTNode.Type.ATOM)

    def is_complete(self) -> bool:
        return self.name() is not None


class Parameter:
    def __init__(self, name: str):
        pass


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


class ExpressionASTNode(ASTNode):
    def __init__(self, node_type: ASTNode.Type):
        super().__init__(node_type=node_type)


class SumASTNode(ExpressionASTNode):
    def __init__(self):
        super().__init__(node_type=ASTNode.Type.SUM)
        self._left: Optional[ExpressionASTNode] = None
        self._right: Optional[ExpressionASTNode] = None

    def left(self) -> Optional[ExpressionASTNode]:
        return self._left

    def set_left(self, left: ExpressionASTNode) -> None:
        self._left = left

    def right(self) -> Optional[ExpressionASTNode]:
        return self._right

    def set_right(self, right: ExpressionASTNode) -> None:
        self._right = right

    def is_complete(self) -> bool:
        return self.left() is not None and self.right() is not None


class StatementASTNode(ASTNode):
    def __init__(self, node_type: ASTNode.Type):
        super().__init__(node_type=node_type)


class ReturnStatementASTNode(StatementASTNode):
    def __init__(self):
        super().__init__(node_type=ASTNode.Type.RETURN_STATEMENT)
        self._expressions: MutableSequence[ExpressionASTNode] = []

    def return_type(self) -> DataType:
        # Calculate this from the expressions
        pass

    def expressions(self) -> MutableSequence[ExpressionASTNode]:
        return self._expressions

    def is_complete(self) -> bool:
        # Return statements can always return nothing, which defaults to None
        return True


class FunctionDefASTNode(StatementASTNode):
    def __init__(self):
        super().__init__(node_type=ASTNode.Type.FUNCTION_DEF)
        self._parameters: MutableSequence[Parameter] = []
        self._statements: MutableSequence[StatementASTNode] = []
        self._return_type: Optional[DataType] = None

    def parameters(self) -> MutableSequence[Parameter]:
        return self._parameters

    def statements(self) -> MutableSequence[StatementASTNode]:
        return self._statements

    def return_type(self) -> DataType:
        if self._return_type is not None:
            return self._return_type

        return DataType(name=DataTypeName.NONE)

    def set_return_type(self, return_type: DataType) -> None:
        self._return_type: DataType = return_type

    def is_complete(self) -> bool:
        return self.name() is not None and self._return_type is not None


class ArgumentASTNode(ASTNode):
    def __init__(self, node_type: ASTNode.Type):
        super().__init__(node_type=node_type)


class FunctionCallASTNode(StatementASTNode):
    def __init__(self):
        super().__init__(node_type=ASTNode.Type.FUNCTION_CALL)
        self._arguments: MutableSequence[ArgumentASTNode] = []

    def arguments(self) -> MutableSequence[ArgumentASTNode]:
        return self._arguments

    def return_type(self) -> DataType:
        # Calculate from function call
        pass

    def is_complete(self) -> bool:
        # Function call doesn't need arguments, but does need a name
        # TODO: or maybe an expression...
        return self.name() is not None
