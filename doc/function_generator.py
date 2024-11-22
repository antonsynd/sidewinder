from dataclasses import dataclass
from io import StringIO
from typing import AbstractSet, Optional, MutableSequence, Sequence, TypeAlias

ArgumentType: TypeAlias = str
ArgumentName: TypeAlias = str
ArgumentDefaultValue: TypeAlias = str
FunctionName: TypeAlias = str
ReturnType: TypeAlias = str


import re

function_signature_pattern = re.compile(r"(.+)\s+([_a-zA-Z][_a-zA-Z0-9]*)\((.+)\)")
function_modifiers: AbstractSet[str] = {
    "static",
    "virtual",
    "final",
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

    def write(self, s: str) -> None:
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
    buffer = CodeStringIO()
    func_name: FunctionName = func_sig.name
    args: Sequence[FunctionArgument] = func_sig.args

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
    buffer.write(f"{proxy_class_name}(std::vector<std::any> args) {{\n")
    buffer.indent()

    for i in range(len(args)):
        buffer.write(f"arg{i}_ = std::any_cast<arg{i}_type>(args[{i}]);\n")

    buffer.dedent()
    buffer.write("}\n")

    buffer.newline()
    buffer.write(f"{proxy_class_name}(std::unordered_map<std::string, std::any> args) {{\n")

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
    buffer.write("}\n")

    return buffer.getvalue()


def generate_function_argument_proxy_from_str(s: str) -> str:
    opt_sig: Optional[FunctionSignature] = parse_function_signature(s=s)

    if not opt_sig:
        return ""

    return generate_function_argument_proxy(func_sig=opt_sig)
