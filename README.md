# sidewinder

Sidewinder is a statically-typed Pythonic language that transpiles to C++20
using [Mamba](https://github.com/antonsynd/mamba) as the standard library
of builtin symbols.

## Dependencies

| Name | Required? | Installation |
| --- | --- | --- |
| `isort` | Yes | `pip install isort` |
| `black` | Yes | `pip install black` |
| `antlr` | Yes | `brew install antlr` |
| `antlr4-python3-runtime` | Yes | `pip install antlr4-python3-runtime` |
| [Github: numba/llvmlite](https://github.com/numba/llvmlite) | Yes | `conda install --channel=numba llvmlite` |
| [Github: antonsynd/chiri](https://github.com/antonsynd/chiri) | Yes | See instructions on [Github](https://github.com/antonsynd/chiri) |
| [Github: antlr/grammars-v4/python/python3_12](https://github.com/antlr/grammars-v4/tree/master/python/python3_12) | Yes | Downloaded during `chiri pkg setup` |
| `pydot` | Optional | `pip install pydot` |
| `graphviz` | Optional | `pip install graphviz && brew install graphviz` |

## Roadmap

Milestones:

1. Go through [LLVM's my first language frontend](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl03.html) to learn the entire stack
2. Design minimal subset of Python that can be typed (e.g. bool, int, float, None)
3. Implement parser with [ANTLR](https://github.com/antlr/grammars-v4/tree/master/python) (or also [ANTLR4 for Python 3.12](https://github.com/RobEin/ANTLR4-parser-for-Python-3.12)) on existing Python 3.13 syntax
4. Add Sidewinder specific extensions to syntax
5. Construct AST from ANTLR parser output
6. Use [llvmlite](https://github.com/numba/llvmlite) to generate LLVM IR
7. Generate LLVM IR code
8. Expand support of typed Python and Sidewinder features
