import sys
from sys import stderr
from pathlib import Path, PurePath as pure_path

x: int = None
y: int = 5


def foo() -> None:
    pass


def bar(x: int, y: int = 5) -> int:
    return x + y


def print(*args, file=sys.stdout) -> None:
    pass


# *args or named args cannot appear after **kwargs, but it can appear before
# unnamed args must appear before named args
def trace(*args, file=sys.stdout, **kwargs) -> None:
    pass


def log(x: int, / y: int) -> None:
    return


if x is int:
    pass
elif y == x:
    pass
else:
    pass


while x:
    break


for x in range(5):
    continue
else:
    pass


try:
    pass
except Exception as e:
    pass


lambda x: x + 2


z = {"a": 5}
w = [2, 5]
u = (5,)

for i, (k, v) in enumerate(z.items()):
    pass


for i in w:
    pass


w[0]
w[0:1:1]
u[0]


bar(5, x = 5)
print(*w)
print(**z)


with (Hello() as hello, Blah()):
    pass
