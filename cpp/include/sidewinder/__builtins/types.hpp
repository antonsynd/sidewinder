#include <type_traits>

struct Complex {
 public:
  int Real() const;
  int Imag() const;
};

template <typename T>
concept Value = std::is_same_v<T, int> || std::is_same_v<T, float> ||
                std::is_same_v<T, bool> || std::is_same_v<T, Complex>;

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
