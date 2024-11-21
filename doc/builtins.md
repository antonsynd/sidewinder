# Sidewinder Builtins

## abs(x)

```C++
int abs(const int x);
float abs(const float x);
Complex abs(const Complex x);

template<typename T, typename U = int>
concept HasAbs = requires(const T& t) {
  { t.__Abs() } -> std::same_as<U>;
};

template<typename T, typename U = int>
requires HasAbs<T, U>
U abs(const std::shared_ptr<T>& x);
```

## aiter(async_iterable)

Not for Sidewinder v1.0

## all(iterable)

```C++
template<typename T>
concept Value = std::is_same_v<T, int>
  || std::is_same_v<T, float>
  || std::is_same_v<T, bool>
  || std::is_same_v<T, std::nullptr_t>
  || std::is_same_v<T, Complex>;

template<typename T>
concept HasBool = requires(const T& t) {
  { t.__Bool() } -> std::same_as<bool>;
};

template<typename T>
concept BoolConvertible = HasBool<T> || Value<T>;

template<typename T, typename U>
concept Iterator = requires(const T& t) {
  // U is U if Value<U> otherwise std::shared_ptr<U>
  { t.__Next() } -> std::same_as<U>;
}

template<typename T, typename U>
concept Iterable = requires(const T& t) {
  { t.__Iter() } -> std::same_as<std::shared_ptr<Iterator<U>>>;
};

template<typename T, typename U>
requires BoolConvertible<U> && Iterable<T, U>
bool all(const std::shared_ptr<T>& iterable);
```

## awaitable anext(async_iterator), awaitable anext(async_iterator, default)

Not for Sidewinder v1.0

## any(iterable)

```C++
template<typename T, typename U>
requires BoolConvertible<U> && Iterable<T<U>>
bool any(const std::shared_ptr<T>& iterable);
```

## ascii(object)

```C++
std::shared_ptr<Str> ascii(const int object);
std::shared_ptr<Str> ascii(const float object);
std::shared_ptr<Str> ascii(const bool object);

template<typename T>
concept HasRepr = requires(const T& t) {
  { t.__Repr() } -> std::same_as<std::shared_ptr<Str>>;
};

template<HasRepr T>
std::shared_ptr<Str> ascii(const std::shared_ptr<T>& object);
```

## bin(x)

```C++
std::shared_ptr<Str> bin(const int x);
std::shared_ptr<Str> bin(const bool x);

template<typename T>
concept HasIndex = requires(const T& t) {
  { t.__Index() } -> std::same_as<int>;
};

template<HasIndex T>
std::shared_ptr<Str> bin(const std::shared_ptr<T>& x);
```

## bool(object=False)

```C++
bool Bool(const int object);
bool Bool(const float object);
bool Bool(const bool object);
bool Bool(const Complex object);
bool Bool(const std::nullptr_t object);

template<HasBool T>
bool Bool(const std::shared_ptr<T>& object);
```

## breakpoint(*args, **kws)

Unsupported in Sidewinder. Sidewinder is not an interpreted language and thus
does not run in a REPL where a debugger can be invoked trivially.

## bytearray(source=b''), bytearray(source, encoding), bytearray(source, encoding, errors)

```C++
std::shared_ptr<ByteArray> ByteArray();
std::shared_ptr<ByteArray> ByteArray(const std::shared_ptr<Bytes>& source);
std::shared_ptr<ByteArray> ByteArray(int source);

// TODO
std::shared_ptr<ByteArray> ByteArray(const std::shared_ptr<BufferInterface>& source);

template<typename T>
requires Iterable<T, int>
std::shared_ptr<ByteArray> ByteArray(const std::shared_ptr<T>& source);

std::shared_ptr<ByteArray> ByteArray(const std::shared_ptr<Str>& source, const std::shared_ptr<Str>& encoding);

// TODO: errors argument
```

## bytes(source=b''), bytes(source, encoding), bytes(source, encoding, errors)

See bytearray.

## callable(object)

Not supported in Sidewinder. The rationale is that this requires a concept to
check if T.__Call() is invocable, but in C++ concepts, all arguments must be
specified. In order to specify them, templating would have to be raised up
to Sidewinder, which is out of the scope that Sidewinder plans to cover.

## chr(i)

```C++
std::shared_ptr<Str> chr(std::shared_ptr<Str> i);
```

## @classmethod

The semantics are slightly different, but this turns it into a static method.

## compile(source, filename, mode, flags=0, dont_inherit=False, optimize=-1)

Not supported in Sidewinder for obvious reasons.

## complex(number=0), complex(string), complex(real=0, imag=0)

```C++
template<typename T>
concept HasComplex = requires(const T& t) {
  { t.__Complex() } -> std::same_as<Complex>;
};

template<typename T>
concept HasFloat = requires(const T& t) {
  { t.__Float() } -> std::same_as<float>;
};

template<typename T>
concept ComplexConvertible = HasComplex<T> || HasFloat<T> || HasIndex<T>;

struct Complex {
 public:
  Complex(const int number = 0, const int real = 0, const int imag = 0);
  Complex(const float number = 0, const float real = 0, const float imag = 0);
  Complex(const bool number = 0, const bool real = 0, const bool imag = 0);
  Complex(const Complex number = 0, const Complex real = 0, const Complex imag = 0);
  Complex(const std::shared_ptr<Str>& string);
};
```

## delattr(object, name)

Not supported in Sidewinder for obvious reasons.

## dict(**kwarg), dict(mapping, **kwarg), dict(iterable, **kwarg)

`**kwarg` is not supported in Sidewinder. Pass in the mapping directly.

```C++
template<typename T, typename K, typename V>
concept Mapping = requires (const T& t, const K& k) {
  // Or V& for Value<V>
  // Also K must be hashable, and either K itself or std::shared_ptr<K>
  { t[k] } -> std::same_as<std::shared_ptr<V>>;
}

template<typename K, typename V>
class Dict {
 public:
  template<typename T>
  requires Mapping<T, K, V>
  Dict(const T& t);

  template<typename T>
  requires Iterable<T, std::shared_ptr<std::tuple<K, V>>>
  Dict(const T& t);
};
```

## dir(), dir(object)

Not supported in Sidewinder. We cannot find local symbols at runtime without
inspecting the symbol table.

## divmod(a, b)

```C++
std::shared_ptr<std::tuple<int, int>> divmod(const int a, const int b);
std::shared_ptr<std::tuple<int, int>> divmod(const float a, const float b);
std::shared_ptr<std::tuple<int, int>> divmod(const int a, const float b);
std::shared_ptr<std::tuple<int, int>> divmod(const float a, const int b);
// TODO: Also for bool arguments
```

## enumerate(iterable, start=0)

```C++
template<typename T>
class Enumerate {};
// __Next() -> std::shared_ptr<std::tuple<int, std::shared_ptr<U>>>

template<typename T, typename U>
requires Iterable<T, U>
Enumerate<U> enumerate(const std::shared_ptr<T>& t, const int start = 0);
```

## eval(source, globals=None, locals=None)

Not supported in Sidewinder for obivous reasons.

## exec(source, globals=None, locals=None, *, closure=None)

Not supported in Sidewinder for obivous reasons.

## filter(function, iterable)
