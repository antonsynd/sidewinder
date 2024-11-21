from typing import Any, Mapping, MutableMapping, MutableSet, Optional, Union

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
        self._current_builder: Optional[ir.IRBuilder] = None
        self._block_names: MutableSet[str] = set()

    def _assert_has_current_builder(self) -> None:
        if not self._current_builder:
            raise ValueError("No current builder")

    def _assert_block_not_defined(self, name: str) -> None:
        if name in self._block_names:
            raise ValueError(f"Cannot define {name} because it already exists in {self._func.name}")

    def current_builder(self) -> ir.IRBuilder:
        self._assert_has_current_builder()

        return self._current_builder

    def add_block(self, name: str = "entry") -> ir.IRBuilder:
        self._assert_block_not_defined(name=name)
        self._block_names.add(name)

        block: ir.Block = self._func.append_basic_block(name=name)
        self._current_builder = ir.IRBuilder(block=block)

        return self._current_builder

    def add_return(self, value: Optional[Any]) -> None:
        builder: ir.IRBuilder = self.current_builder()

        if value is not None:
            builder.ret(value)
        else:
            builder.ret_void()


class ModuleCodeGenerator:
    def __init__(self, module: ir.Module):
        self._module: ir.Module = module

    def module(self) -> ir.Module:
        return self._module

    def dump(self) -> str:
        return str(self.module())

    def _assert_global_name_undefined(self, name: str) -> None:
        try:
            self._module.get_global(name=name)
            raise ValueError(
                f"Cannot define {name} because it already exists in {self._module.name}"
            )
        except KeyError:
            # We want this to not exist, so pass
            pass

    def add_global_variable(
        self,
        ir_type: ir.Type,
        name: str,
        initializer: GlobalVariableInitializer,
    ) -> ir.GlobalVariable:
        self._assert_global_name_undefined(name=name)

        global_var = ir.GlobalVariable(module=self.module(), typ=ir_type, name=name)
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
        self._assert_global_name_undefined(name=name)

        return FunctionCodeGenerator(module=self.module(), name=name, func_type=func_type)


class CodeGenerator:
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

    def _assert_has_no_current_module(self) -> None:
        if self._current_module:
            raise RuntimeError(f"Module {self._current_module.name} is currently open")

    def current_module(self) -> ir.Module:
        self._assert_has_current_module()

        return self._current_module

    def _assert_module_name_does_not_exist(self, name: str) -> None:
        if name in self._modules:
            raise ValueError(f"Module {name} already exists")

    def _assert_module_name_exists(self, name: str) -> None:
        if name in self._modules:
            raise ValueError(f"Module {name} does not exist")

    def dump_modules(self) -> Mapping[str, str]:
        return {name: str(module) for name, module in self._modules.items()}

    def _open_module_unchecked(self, module: ir.Module) -> ModuleCodeGenerator:
        self._current_module = module

        return ModuleCodeGenerator(module=self._current_module)

    def add_module(
        self, name: str, open_module: bool = False
    ) -> Union[ir.Module, ModuleCodeGenerator]:
        self._assert_module_name_does_not_exist(name=name)

        module = ir.Module(name=name)
        module.triple = self._triple
        self._modules[name] = module

        if open_module:
            return self._open_module_unchecked(module=module)

        return module

    def open_module(self, name: str) -> ModuleCodeGenerator:
        self._assert_module_name_exists(name=name)
        self._assert_has_no_current_module()

        return self._open_module_unchecked(module=self._modules[name])

    def close_module(self, raise_if_noop: bool = False) -> None:
        if raise_if_noop:
            self._assert_has_current_module()

        self._current_module = None
