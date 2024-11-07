# sidewinder

Sidewinder is a statically-typed Pythonic language that targets LLVM IR.

# Dependencies

* isort
* black
* [Chiri](https://github.com/antonsynd/chiri)

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
