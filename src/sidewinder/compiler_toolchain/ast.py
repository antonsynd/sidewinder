from typing import Optional, Sequence


class ASTNode:
    def __init__(self, name: str, children: Optional[Sequence["ASTNode"]] = None):
        self.name: str = name
        self.children: Sequence[ASTNode] = children if children else []

    def __repr__(self):
        return f"{self.name} -> ({', '.join(map(str, self.children))})"
