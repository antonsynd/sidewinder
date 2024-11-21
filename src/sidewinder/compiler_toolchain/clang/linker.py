import subprocess
from pathlib import Path
from typing import Optional, Sequence

from sidewinder.compiler_toolchain.linker import LinkerBase


class ClangLinker(LinkerBase):
    def __init__(self, clang_path: Optional[Path]):
        super().__init__()
        self._clang_path: Optional[Path] = clang_path

    def link(self, objects: Sequence[Path], output: Path) -> None:
        clang_args: Sequence[str] = []

        if self._clang_path:
            clang_args.append(str(self._clang_path))
        else:
            clang_args.append("clang")

        clang_args.extend([str(obj) for obj in objects])
        clang_args.extend(["-o", str(output)])

        subprocess.run(args=clang_args, check=True)
