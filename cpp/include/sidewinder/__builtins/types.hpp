#include <cstddef>
#include <memory>
#include <optional>
#include <type_traits>

using Int = int;
using Bool = bool;
using Float = float;

struct Complex {
 public:
  Int Real() const { return real_; }
  Int Imag() const { return imag_; }

 private:
  Int real_;
  Int imag_;
};

template <typename T>
concept Value = std::is_same_v<T, Int> || std::is_same_v<T, Float> ||
                std::is_same_v<T, Bool> || std::is_same_v<T, Complex>;

template <typename T>
concept Object = !Value<T>;

template <Object T>
using Reference = std::shared_ptr<T>;

template <typename T>
using Optional = std::conditional_t<std::optional<T>, Reference<T>>;

template <typename T>
using Const = std::conditional_t<Value<T>, const T, const Reference<T>&>;

template <typename T>
using Mutable = std::conditional_t<Value<T>, T, Reference<T>>;

template <typename T>
constexpr auto kNone = std::conditional_t<Value<T>, std::nullopt, std::nullptr>;
