# Sidewinder language specification

## 1. Variables

### 1.1. Declaration and definition

A variable in Sidewinder is declared like so:

```Python
foobar: int = 5
```

In addition to a declaration, in top-level code (i.e. module level), a
variable must be defined with a value or expression.

The type annotation is optional, as it will be inferred at compile-time. The
compiler will always pick the most specific instantiation of the given type.

For types that have conflicting literal representations, e.g. `int`, `bigint`,
`byte`, `float`, and `double`, the following subscripts can be used to specify
which type is desired:

```Python
foobar = 5i    # int
foobar = 5b    # byte
foobar = 5bi   # bigint
foobar = 5.0f  # float
foobar = 5.0d  # double
```

By default, integer values are `int` and floating point values are `float`.

### 1.2. Assignment

Variables can be assigned with the assignment operator `=`.

```Python
foobar = 7
```

Subsequent assignments (after the initial declaration and definition) do not
need a type declaration. However, if a type declaration is added, and it is
different from the original type declaration, then the new type declaration
shadows the old one (similar to Rust variable shadowing). This emulates the
duck typing behavior in Python, but in a statically-typed way.

```Python
foobar: Optional[int] = get_optional_int()
foobar: int = foobar.value_or(0)
```

### 1.3. Variable names

Variables in Sidewinder must adhere to the following PCRE regex:
`/[a-zA-Z_][a-zA-Z0-9_]*/`.

Additionally, variable names have semantics attached to them, formalizing
existing Python conventions. Variables prefixed with a single underscore
implicitly have `protected` access, whereas variables prefixed with two
underscores implicitly have `private` access (including dunder methods).
Variables with a name in all caps (and underscores) are `const`.

### 1.4. Access modifiers

Sidewinder doesn't have explicit access modifiers. They are encoded directly
into the variable name.

`const` variables cannot be reassigned, but if they represent an object, that
object can be mutated internally. Variables are `mutable` by default.

`private` variables are visible only to the module in which they are declared
if they are at the module-level, and only to the immediate class in which they
are defined.

`protected` variables are visible only to the project in which they are
declared (essentially `internal`), and only to the immediate class and any of
its subclasses, the former of which it is defined in.

`public` variables are visible to all consumers.

### 2. Functions

### 2.1. Declaration and definition

Functions are declared and defined like so:

```Python
def foobar(x: int, y: int) -> int:
    return x + y
```

The return type is optional if it can be inferred from all `return`
(or `yield`) statements in the function body. By default, a function that
returns no value returns the special internal type `void`, which is not
visible to the programmer.

Functions are a first-class member of the type system and can be represented
as a type themselves.

```Python
type FoobarFunc = Function[(int, int), int]  # C++ std::function<(int)(int, int)>
```

A function that has no return value (i.e. `void`) omits the return type in the
function type. It is understood to be `void` internally.

```Python
type DummyFunc = Function[(int)]  # C++ std::function<(void)(int)>
```
