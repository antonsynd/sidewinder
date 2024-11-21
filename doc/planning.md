# Sidewinder language planning

| Feature | Subfeature | Milestone | Notes |
| --- | --- | --- | --- |
| int | type | v0.1 | int32 only, and no class methods |
| float | type | v0.1 | float32 only, and no class methods |
| bool | type | v0.1 | no class methods |
| operators | N/A | v0.1 | =, +, -, *, / |
| operators | N/A | v0.1 | ==, and, or, not, is |
| variables | N/A | v0.1 | N/A |
| function | def | v0.1 | Named and typed arguments, no default args, return type |
| function | call | v0.1 | No named arguments |
| print | N/A | v0.1 | only to stdout |
| if, elif, else | N/A | v0.1 | N/A |
| while | N/A | v0.1 | N/A |
| for | N/A | v0.2 | N/A |
| str | type | v0.2 | literals only |
| tuple | type | v0.2 | some methods only |
| list | type | v0.2 | some methods only |
| set | type | v0.2 | some methods only |
| dict | type | v0.2 | some methods only |
| try, except, finally | N/A | v0.3 | N/A |
| with | N/A | v0.4 | N/A |

| Sidewinder type | C++ ABI type | Notes |
| --- | --- | --- |
| `int` | `int` | |
| `float` | `float` | |
| `bool` | `bool` | |
| `None` | `void` | For function return type |
| `None` | `std::shared_ptr<T>(nullptr)` | For object values and return values. Note that `int`, `float`, and `bool` cannot store `None` |
| `T` object | `std::shared_ptr<T>` | |
| `T?` optional | `std::optional<T>` | For all primitive types except `None` |
| `T?` optional object | `std::shared_ptr<T>` | For object types |

Object types of type `T` in Sidewinder are always `std::shared_ptr<T>`.
Syntactic `None` assignment/return values are not allowed.

Optional object types of type `T?` in Sidewinder are always `std::shared_ptr<T>`.
Syntactic `None` assignment/return values results in internal `nullptr` assignment.

Primitive types of type `T` in Sidewinder are always their corresponding C++ type.
Syntactic `None` assignment/return values are not allowed.

Optional object types of type `T?` in Sidewinder are always `std::optional<T>`.
Syntactic `None` assignment/return values results in internal `std::nullopt` assignment.
