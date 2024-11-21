from dataclasses import dataclass
from typing import Any, Callable, TypeAlias, Union

from llvmlite import ir

INT8_T: ir.Type = ir.IntType(8)
INT32_T: ir.Type = ir.IntType(32)
INT64_T: ir.Type = ir.IntType(64)
FLOAT32_T: ir.Type = ir.FloatType()
FLOAT64_T: ir.Type = ir.DoubleType()
VOID_T: ir.Type = ir.VoidType()


def PTR_T(pointee: ir.Type) -> ir.PointerType:
    return ir.PointerType(pointee=pointee)


GlobalVariableInitializerFunc: TypeAlias = Callable[[], ir.Constant]


@dataclass
class ConstantValueArgs:
    ir_type: ir.Type
    constant: Any


GlobalVariableInitializer: TypeAlias = Union[GlobalVariableInitializerFunc, ConstantValueArgs]
