import sys

def add(x: int, y: int) -> int:
    return x + y

z: int = 3
res = add(1, z)

print(res, file=sys.stdout)
