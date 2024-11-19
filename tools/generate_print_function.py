#!/usr/bin/env python3
import argparse
from pathlib import Path
import subprocess

from llvmlite import ir, binding


def main() -> None:
    args = parse_args()

    codegen(object_path=args.object)
    link(object_path=args.object, program_path=args.program)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-o", "--object", type=Path, required=True)
    parser.add_argument("-p", "--program", type=Path, required=True)

    return parser.parse_args()


def codegen(object_path: Path) -> None:
    # Initialize LLVM bindings
    binding.initialize()
    binding.initialize_native_target()
    binding.initialize_native_asmprinter()

    # Specify the target triple for macOS on Apple Silicon
    macos_target_triple = "arm64-apple-macosx15.0.0"

    # Create an LLVM module
    module = ir.Module(name="printf_example")
    module.triple = macos_target_triple

    # Declare the printf function
    printf_type = ir.FunctionType(ir.IntType(32), [ir.PointerType(ir.IntType(8))], var_arg=True)
    printf_func = ir.Function(module, printf_type, name="printf")

    # Declare the atoi function (to convert strings to integers)
    atoi_type = ir.FunctionType(ir.IntType(32), [ir.PointerType(ir.IntType(8))])
    atoi_func = ir.Function(module, atoi_type, name="atoi")

    # Define the call_printf function
    func_type = ir.FunctionType(ir.VoidType(), [ir.IntType(32), ir.IntType(32)])
    call_printf_func = ir.Function(module, func_type, name="call_printf")

    block = call_printf_func.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)

    # Define the format string
    format_str = "%d, %d\n\0"
    format_str_global = ir.GlobalVariable(
        module, ir.ArrayType(ir.IntType(8), len(format_str)), name="format_str"
    )
    format_str_global.global_constant = True
    format_str_global.initializer = ir.Constant(
        ir.ArrayType(ir.IntType(8), len(format_str)), bytearray(format_str.encode("utf8"))
    )

    # Get a pointer to the format string
    format_str_ptr = builder.bitcast(format_str_global, ir.PointerType(ir.IntType(8)))

    # Call printf with the format string and arguments
    builder.call(printf_func, [format_str_ptr, call_printf_func.args[0], call_printf_func.args[1]])
    builder.ret_void()

    # Define the main function
    main_type = ir.FunctionType(
        ir.IntType(32), [ir.IntType(32), ir.PointerType(ir.PointerType(ir.IntType(8)))]
    )
    main_func = ir.Function(module, main_type, name="main")

    block = main_func.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)

    # Parse command-line arguments
    argc, argv = main_func.args[0], main_func.args[1]
    arg1_ptr = builder.gep(argv, [ir.Constant(ir.IntType(32), 1)])  # argv[1]
    arg2_ptr = builder.gep(argv, [ir.Constant(ir.IntType(32), 2)])  # argv[2]

    arg1_str = builder.load(arg1_ptr)
    arg2_str = builder.load(arg2_ptr)

    arg1_int = builder.call(atoi_func, [arg1_str])
    arg2_int = builder.call(atoi_func, [arg2_str])

    # Call call_printf with the parsed integers
    builder.call(call_printf_func, [arg1_int, arg2_int])

    # Return 0 from main
    builder.ret(ir.Constant(ir.IntType(32), 0))

    # Print the generated LLVM IR (optional)
    print("Generated LLVM IR:")
    print(module)

    # Compile the IR to an object file
    llvm_ir = str(module)
    llvm_module = binding.parse_assembly(llvm_ir)
    llvm_module.verify()

    # Set up a target machine
    target = binding.Target.from_triple(macos_target_triple)
    target_machine = target.create_target_machine()

    # Generate object code
    object_path.write_bytes(target_machine.emit_object(llvm_module))
    print(f"Object file written to {object_path}")


def link(object_path: Path, program_path: Path) -> None:
    subprocess.run(["clang", str(object_path), "-o", str(program_path)], check=True)
    print(f"Linked file written to {program_path}")


if __name__ == "__main__":
    main()
