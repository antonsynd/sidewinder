#!/usr/bin/env python3
import argparse
import sys
from dataclasses import dataclass
from io import StringIO
from typing import AbstractSet, Optional, MutableSequence, Sequence, TypeAlias

ArgumentType: TypeAlias = str
ArgumentName: TypeAlias = str
ArgumentDefaultValue: TypeAlias = str
FunctionName: TypeAlias = str
ReturnType: TypeAlias = str


import re

function_signature_pattern = re.compile(r"(.+)\s+([_a-zA-Z][_a-zA-Z0-9]*)\((.*)\)")
function_modifiers: AbstractSet[str] = {
    "static",
    "virtual",
    "final",
    "constexpr",
    "inline",
}
argument_pattern = re.compile(r"(.+)\s+([_a-zA-Z][_a-zA-Z0-9]*)(?:\s+=\s+(.+))?")


@dataclass
class FunctionArgument:
    arg_type: ArgumentType
    name: ArgumentName
    default_value: ArgumentDefaultValue


@dataclass
class FunctionSignature:
    name: FunctionName
    args: Sequence[FunctionArgument]
    return_type: ReturnType


def parse_arguments(args_str: str, dest: MutableSequence[FunctionArgument]) -> None:
    args: Sequence[str] = args_str.split(",")

    for i, arg in enumerate(args):
        res = argument_pattern.match(arg)

        if not res:
            raise Exception(f"Unable to parse argument {i}: {arg}")

        arg_type, arg_name, arg_default_val = res.groups()

        dest.append(
            FunctionArgument(
                arg_type=arg_type.strip(),
                name=arg_name,
                default_value=arg_default_val.strip() if arg_default_val else "",
            )
        )


def parse_function_signature(s: str) -> Optional[FunctionSignature]:
    res = function_signature_pattern.match(s)

    if not res:
        return None

    prefix, name, args = res.groups()

    return_type_components: MutableSequence[str] = []
    for comp in prefix.split():
        if comp in function_modifiers:
            continue

        return_type_components.append(comp)

    return_type: ReturnType = " ".join(return_type_components)

    args = args.strip()

    func_args: MutableSequence[FunctionArgument] = []

    if args:
        parse_arguments(args_str=args, dest=func_args)

    return FunctionSignature(name=name.strip(), args=func_args, return_type=return_type.strip())


class CodeStringIO:
    def __init__(self):
        self._buffer = StringIO()
        self._indent: str = ""

    def write(self, s: str, no_indent: bool = False) -> None:
        if not no_indent:
            self._write_indent()

        self._buffer.write(s)

    def newline(self) -> None:
        self._buffer.write("\n")

    def indent(self, n: int = 2) -> None:
        self._indent += " " * n

    def dedent(self, n: int = 2) -> None:
        if len(self._indent) >= n:
            self._indent = self._indent[n:]
        else:
            self._indent = ""

    def getvalue(self) -> str:
        return self._buffer.getvalue()

    def _write_indent(self) -> None:
        self._buffer.write(self._indent)


def generate_function_argument_proxy(func_sig: FunctionSignature) -> str:
    args: Sequence[FunctionArgument] = func_sig.args
    num_args: int = len(args)

    if not num_args:
        # No need for argument proxy if there are no args
        return ""

    buffer = CodeStringIO()
    func_name: FunctionName = func_sig.name

    proxy_class_name: str = f"__FunctionArgs__{func_name}"

    buffer.write(
        f"""class {proxy_class_name} {{
 public:
"""
    )

    buffer.indent()

    for i, arg in enumerate(args):
        buffer.write(f"using arg{i}_type = {arg.arg_type};\n")

    buffer.newline()
    buffer.write(f"explicit {proxy_class_name}(std::vector<std::any> args) {{\n")
    buffer.indent()

    for i in range(len(args)):
        buffer.write(f"arg{i}_ = std::any_cast<arg{i}_type>(args[{i}]);\n")

    buffer.dedent()
    buffer.write("}\n")

    buffer.newline()
    buffer.write(
        f"explicit {proxy_class_name}(std::unordered_map<std::string, std::any> args) {{\n"
    )

    buffer.indent()
    for i, arg in enumerate(args):
        buffer.write(f'arg{i}_ = std::any_cast<arg{i}_type>(args.at("{arg.name}"));\n')

    buffer.dedent()
    buffer.write("}\n")

    buffer.newline()
    for i in range(len(args)):
        buffer.write(f"arg{i}_type Arg{i}() const {{ return arg{i}_; }}\n")

    buffer.dedent()
    buffer.indent(n=1)

    buffer.newline()
    buffer.write("private:\n")
    buffer.indent(n=1)

    for i in range(len(args)):
        buffer.write(f"arg{i}_type arg{i}_;\n")

    buffer.dedent()
    buffer.write("};\n")

    return buffer.getvalue()


def generate_function_argument_proxy_from_str(s: str) -> str:
    opt_sig: Optional[FunctionSignature] = parse_function_signature(s=s)

    if not opt_sig:
        return ""

    return generate_function_argument_proxy(func_sig=opt_sig)


def _generate_arg_forwarding_body(
    buffer: CodeStringIO, args_class_name: str, num_args: int
) -> None:
    buffer.indent()
    buffer.write(f"{args_class_name} arg_helper(std::move(args));\n")

    buffer.newline()

    if num_args:
        buffer.write(f"return func_(\n")

        buffer.indent()

        for i in range(num_args - 1):
            buffer.write(f"arg_helper.Arg{i}(),\n")

        buffer.write(f"arg_helper.Arg{num_args - 1}());\n")
        buffer.dedent()
    else:
        buffer.write(f"return func_();\n")

    buffer.dedent()


def generate_function_invocable_proxy(func_sig: FunctionSignature) -> str:
    buffer = CodeStringIO()
    func_name: FunctionName = func_sig.name
    return_type: ReturnType = func_sig.return_type
    args: Sequence[FunctionArgument] = func_sig.args
    num_args: int = len(args)

    args_class_name: str = f"__FunctionArgs__{func_name}"
    proxy_class_name: str = f"__FunctionProxy__{func_name}"
    user_implementation_name: str = f"__UserFunctionImplementation__{func_name}"

    buffer.write(f"struct {proxy_class_name} : public FunctionBase {{\n")

    buffer.indent(n=1)
    buffer.write("public:\n")

    buffer.indent(n=1)
    buffer.write(f"using return_type = {return_type};\n")

    for i in range(num_args):
        buffer.write(f"using arg{i}_type = {args_class_name}::arg{i}_type;\n")

    buffer.newline()
    buffer.write(f"{proxy_class_name}() : func_({user_implementation_name}) {{}}\n")

    buffer.newline()

    if num_args:
        buffer.write("return_type operator()(std::vector<std::any> args) const {\n")
        _generate_arg_forwarding_body(
            buffer=buffer, args_class_name=args_class_name, num_args=num_args
        )
        buffer.write("}\n")
    else:
        buffer.write("return_type operator()(std::vector<std::any>) const { return func_(); }\n")

    buffer.newline()

    if num_args:
        buffer.write(
            f"return_type operator()(std::unordered_map<std::string, std::any> args) const {{\n"
        )
        _generate_arg_forwarding_body(
            buffer=buffer, args_class_name=args_class_name, num_args=num_args
        )
        buffer.write("}\n")
    else:
        buffer.write(
            "return_type operator()(std::unordered_map<std::string, std::any>) const { return func_(); }\n"
        )

    buffer.newline()

    if num_args:
        buffer.write("return_type operator()(\n")
        buffer.indent(n=4)

        for i, arg in enumerate(args[:-1]):
            buffer.write(f"arg{i}_type {arg.name},\n")

        buffer.write(f"arg{i}_type {args[-1].name}) const {{\n")
        buffer.dedent()

        buffer.write("return func_(\n")
        buffer.indent()

        for arg in args[:-1]:
            buffer.write(f"{arg.name},\n")

        buffer.write(f"{args[-1].name});\n")
        buffer.dedent(n=4)
        buffer.write("}\n")
    else:
        buffer.write("return_type operator()() const { return func_(); }\n")

    buffer.newline()
    buffer.dedent(n=1)
    buffer.write("private:\n")
    buffer.indent(n=1)

    if num_args:
        buffer.write(f"std::function<{return_type}(\n")
        buffer.indent(n=4)

        for i, arg in enumerate(args[:-1]):
            buffer.write(f"{arg.arg_type},\n")

        buffer.write(f"{args[-1].arg_type})> func_;\n")
        buffer.dedent(n=4)
    else:
        buffer.write(f"std::function<{return_type}()> func_;\n")

    buffer.dedent()
    buffer.write("};\n")
    buffer.dedent()

    buffer.newline()
    buffer.write(f"const {proxy_class_name} {func_name};\n")

    return buffer.getvalue()


def generate_function_invocable_proxy_from_str(s: str) -> str:
    opt_sig: Optional[FunctionSignature] = parse_function_signature(s=s)

    if not opt_sig:
        return ""

    return generate_function_invocable_proxy(func_sig=opt_sig)


def main() -> None:
    args: argparse.Namespace = parse_args()
    input_sig: str = args.input

    opt_sig: Optional[FunctionSignature] = parse_function_signature(s=input_sig)

    if not opt_sig:
        print(f"Function signature is invalid", file=sys.stderr)
        sys.exit(1)

    print(generate_function_argument_proxy(func_sig=opt_sig))
    print(generate_function_invocable_proxy(func_sig=opt_sig))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input", type=str, required=True, help="The C++ function signature."
    )

    return parser.parse_args()


if __name__ == "__main__":
    main()
