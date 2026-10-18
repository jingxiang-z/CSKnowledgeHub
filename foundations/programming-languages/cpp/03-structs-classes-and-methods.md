# 03 Structs, Classes, and Methods

Classes combine data with operations and can enforce rules through constructors and access control. Use a simple struct when its fields can vary independently without violating an invariant.

## Construct a Valid Object

```cpp
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>

class Book {
public:
    explicit Book(std::string title) : title_(std::move(title)) {
        if (title_.empty()) {
            throw std::invalid_argument("Title must not be empty");
        }
    }

    const std::string& title() const {
        return title_;
    }

    void check_out() {
        if (checked_out_) {
            throw std::logic_error("Already checked out");
        }
        checked_out_ = true;
    }

private:
    std::string title_;
    bool checked_out_ = false;
};

int main() {
    Book book{"Systems notes"};
    book.check_out();
    std::cout << book.title() << '\n';
}
```

The constructor's initializer list initializes members before its body runs. Members initialize in declaration order, regardless of their order in that list. `explicit` prevents this constructor from being used for unintended implicit conversions. `std::move` enables transferring the parameter's string resources into the member; chapter 7 explains moves.

## Access and Const Methods

`private` members are accessible to the class and its friends. `public` operations define the external API. A `class` defaults to private member access; a `struct` defaults to public access. Otherwise they support the same language facilities.

The trailing `const` on `title()` permits calling it on a const `Book` and prevents ordinary modification of members through that method. The returned reference avoids copying, but its validity depends on the book's lifetime; chapter 4 explains borrowed access.

Prefer composition when one type contains another. Use inheritance when a substitutable interface is required, as shown in chapter 8. Let standard member types handle their own cleanup instead of writing unnecessary destructors.

[Next: Lifetimes, References, and RAII](04-lifetimes-references-and-raii.md)

## References

- [C++ Core Guidelines: Classes and class hierarchies](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-class)
- [C++ Core Guidelines: Constructors](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-ctor)
