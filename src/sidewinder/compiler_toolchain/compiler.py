from typing import Optional, Union

from llvmlite.binding import ModuleRef, Target, TargetMachine, parse_assembly


class Compiler:
    def __init__(self, triple: str):
        self._triple: str = triple
        self._target: Target = Target.from_triple(triple=self._triple)
        self._target_machine: TargetMachine = self._target.create_target_machine()

    def triple(self) -> str:
        return self._triple

    def compile(self, module: Union[str, ModuleRef]) -> bytes:
        ref: Optional[ModuleRef] = None

        if isinstance(module, str):
            ref = parse_assembly(module)
            ref.verify()
        elif isinstance(module, ModuleRef):
            ref = module
        else:
            raise ValueError("module argument must either LLVM IR string or a module ref")

        return self._target_machine.emit_object(module=ref)
