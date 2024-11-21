from enum import Enum
from typing import Sequence, Type

import llvmlite
from llvmlite import binding, ir


class BuiltInTypeName(Enum):
    INT = ir.IntType(32)
    NONE = ir.VoidType()


class CodeGenerator:
    def __init__(self):
        binding.initialize()
        binding.initialize_native_target()
        binding.initialize_native_asmprinter()

    def codegen_print(args: Sequence[int]) -> None:
        module = ir.Module(name="builtins")
        module.triple = binding.get_default_triple()

        int8_t = ir.IntType(8)
        int32_t = ir.IntType(32)
        void_t = ir.VoidType()

        printf_t = ir.FunctionType(int32_t, [ir.PointerType(int8_t)], var_arg=True)
        printf = ir.Function(module, printf_t, name="printf")
        block = printf.append_basic_block(name="entry")
        builder = ir.IRBuilder(block)

        func_ty = ir.FunctionType(void_t, [int32_t] * len(args))
        print_func = ir.Function(module, func_ty, name=f"__print_{len(args)}_ints")

        # Prepare the format string
        fmt: str = " ".join("%d" * len(args)) + "\n\0"
        fmt_global = ir.GlobalVariable(
            module, ir.ArrayType(int8_t, len(fmt)), name=f"__{len(args)}_int_fmt"
        )
        fmt_global.initializer = ir.Constant(
            ir.ArrayType(int8_t, len(fmt)), bytearray(fmt.encode("utf-8"))
        )
        fmt_global.global_constant = True

        fmt_ptr = builder.bitcast(fmt_global, ir.PointerType(int8_t))

        builder.call(printf, [fmt_ptr, *print_func.args])
        builder.ret_void()

        llvm_ir = str(module)
        print("Generated LLVM IR:")
        print(llvm_ir)

        target = binding.Target.from_triple(module.triple)
        target_machine = target.create_target_machine()

        mod = binding.parse_assembly(llvm_ir)
        mod.verify()

        with open("output.o", "wb") as f:
            obj_code = target_machine.emit_object(mod)
            f.write(obj_code)
