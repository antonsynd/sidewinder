from typing import Any, Mapping, MutableMapping, MutableSet, Optional, Sequence, Tuple

from llvmlite import binding, ir

from sidewinder.compiler_toolchain.codegen.types import (
    INT8_T,
    INT32_T,
    VOID_T,
    ConstantValueArgs,
    GlobalVariableInitializer,
    GlobalVariableInitializerFunc,
)


class FunctionCodeGenerator:
    def __init__(self, module: ir.Module, name: str, func_type: ir.FunctionType):
        self._module: ir.Module = module
        self._func: ir.Function = ir.Function(module=self._module, ftype=func_type, name=name)

        self._current_block: Optional[ir.Block] = None
        self._current_builder: Optional[ir.IRBuilder] = None
        self._block_names: MutableSet[str] = set()

    def _assert_has_current_block(self) -> None:
        if not self._current_block:
            raise ValueError("No current block")

    def _assert_has_current_builder(self) -> None:
        if not self._current_builder:
            raise ValueError("No current builder")

    def _assert_block_not_defined(self, name: str) -> None:
        if name in self._block_names:
            raise ValueError(f"Cannot define {name} because it already exists in {self._func.name}")

    def current_block(self) -> ir.Block:
        self._assert_has_current_block()

        return self._current_block

    def current_builder(self) -> ir.IRBuilder:
        self._assert_has_current_builder()

        return self._current_builder

    def add_block(self, name: str = "entry") -> Tuple[ir.Block, ir.IRBuilder]:
        self._assert_block_not_defined(name=name)
        self._block_names.add(name)

        self._current_block: ir.Block = self._func.append_basic_block(name=name)
        self._current_builder = ir.IRBuilder(block=self._current_block)

        return self._current_block, self._current_builder

    def add_return(self, value: Optional[Any]) -> None:
        builder: ir.IRBuilder = self.current_builder()

        if value is not None:
            builder.ret(value)
        else:
            builder.ret_void()


class ModuleCodeGenerator:
    def __init__(self, triple: str):
        binding.initialize()
        binding.initialize_native_target()
        binding.initialize_native_asmprinter()

        self._triple: str = triple
        self._modules: MutableMapping[str, ir.Module] = dict()
        self._current_module: Optional[ir.Module] = None

    def triple(self) -> str:
        return self._triple

    def finalize(self):
        binding.shutdown()

    def _assert_has_current_module(self) -> None:
        if not self._current_module:
            raise RuntimeError("No current module open")

    def current_module(self) -> ir.Module:
        self._assert_has_current_module()

        return self._current_module

    def create_module(self, name: str) -> ir.Module:
        if name in self._modules:
            raise ValueError("Module {name} already exists")

        module = ir.Module(name=name)
        module.triple = self._triple
        self._modules[name] = module

        return module

    def open_module(self, name: str) -> ir.Module:
        if name not in self._modules:
            raise ValueError("Module {name} does not exist")

        self._current_module = self._modules[name]

        return self._current_module

    def dump_module(self, name: str) -> str:
        if name not in self._modules:
            raise ValueError(f"Module {name} does not exist")

        return str(self._modules[name])

    def dump_modules(self) -> Mapping[str, str]:
        return {name: str(module) for name, module in self._modules.items()}

    def _assert_global_name_undefined(self, name: str, module: Optional[ir.Module] = None) -> None:
        """
        Ensures that the given module (or current module if none was passed in)
        does not have a global value with the given name.

        :param name The name to check in the module.
        :param module Optional reference to the current module to avoid
                      excessive checks for the current module.
        """
        if not module:
            module = self.current_module()

        try:
            module.get_global(name=name)
            raise ValueError(f"Cannot define {name} because it already exists in {module.name}")
        except KeyError:
            # We want this to not exist, so pass
            pass

    def add_global_variable(
        self,
        ir_type: ir.Type,
        name: str,
        initializer: GlobalVariableInitializer,
    ) -> ir.GlobalVariable:
        module: ir.Module = self.current_module()
        self._assert_global_name_undefined(name=name, module=module)

        global_var = ir.GlobalVariable(module=self.current_module(), typ=ir_type, name=name)
        global_var.global_constant = True

        if isinstance(initializer, GlobalVariableInitializerFunc):
            global_var.initializer = initializer()
        elif isinstance(initializer, ConstantValueArgs):
            global_var.initializer = initializer
        else:
            raise ValueError(
                "initializer must either be a global variable initializer "
                "function or constant value arguments"
            )

        return global_var

    def add_global_function(self, name: str, func_type: ir.FunctionType) -> FunctionCodeGenerator:
        module: ir.Module = self.current_module()

        return FunctionCodeGenerator(module=module, name=name, func_type=func_type)
