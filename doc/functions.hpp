#include <any>
#include <functional>
#include <string>
#include <vector>

int __UserFunctionImplementation__add(int x, int y) {
  return x + y;
}

class __FunctionArgs__add {
 public:
  using arg0_type = int;
  using arg1_type = int;

  __FunctionArgs__add(std::vector<std::any> args) {
    arg0_ = std::any_cast<arg0_type>(args[0]);
    arg1_ = std::any_cast<arg1_type>(args[1]);
  }

  __FunctionArgs__add(std::unordered_map<std::string, std::any> args) {
    arg0_ = std::any_cast<arg0_type>(args.at("x"));
    arg1_ = std::any_cast<arg1_type>(args.at("y"));
  }

  arg0_type Arg0() const { return arg0_; }
  arg1_type Arg1() const { return arg1_; }

 private:
  arg0_type arg0_;
  arg1_type arg1_;
};

class FunctionBase {
 public:
  virtual ~FunctionBase() = default;
};

struct Str {
 public:
  using storage = std::string;

  operator std::string() const { return s_; }

 private:
  storage s_;
};

// Every tuple extends this, and implements accessors?
struct TupleBase {
 public:
  using storage = std::vector<std::any>;

  virtual ~TupleBase() = default;

  std::any operator[](const int index) const { return elems_[index]; }

 private:
  mutable storage elems_;
};

template <typename K, typename V>
struct DictItemBase : public TupleBase {
 public:
  virtual ~DictItemBase() = default;

  // how to check for equality?
};

// generated at compile time
template <typename K, typename V>
struct DictItem : public DictItemBase<K, V> {
 public:
  using elem0_type = K;
  using elem1_type = V;

  // opposite of std::tie
  std::tuple<elem0_type, elem1_type> Wrap() {
    return std::make_tuple<elem0_type, elem1_type>(
        std::any_cast<elem0_type>(this->operator[](0)),
        std::any_cast<elem1_type>(this->operator[](1)));
  }
};

struct __FunctionProxy__add : public FunctionBase {
 public:
  __FunctionProxy__add() : func_(__UserFunctionImplementation__add) {}

  using return_type = int;
  using arg0_type = __FunctionArgs__add::arg0_type;
  using arg1_type = __FunctionArgs__add::arg1_type;

  return_type operator()(std::vector<std::any> args) const {
    __FunctionArgs__add arg_helper(std::move(args));

    return func_(arg_helper.Arg0(), arg_helper.Arg1());
  }

  return_type operator()(std::unordered_map<std::string, std::any> args) const {
    __FunctionArgs__add arg_helper(std::move(args));

    return func_(arg_helper.Arg0(), arg_helper.Arg1());
  }

  return_type operator()(arg0_type x, arg1_type y) const { return func_(x, y); }

  std::function<int(int, int)> func_;
};

const __FunctionProxy__add add;

// Questions, how do we pass this around? Simply passing copies is viable
// or wrap it in std::function itself --> therefore it is a value that is
// copyable
// any object that implements __Call()...? maybe Call() invokes operator()
