from llvmlite.binding import ModuleRef, Target, TargetMachine


class Compiler:
    def __init__(self, triple: str):
        self._triple: str = triple
        self._target: Target = Target.from_triple(triple=self._triple)
        self._target_machine: TargetMachine = self._target.create_target_machine()

    def compile(self, module: ModuleRef) -> bytes:
        return self._target_machine.emit_object(module)
