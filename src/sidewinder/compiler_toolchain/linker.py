from pathlib import Path
from typing import Sequence


class LinkerBase:
    def __init__(self):
        pass

    def link(objects: Sequence[Path], output: Path) -> None:
        raise NotImplementedError()
