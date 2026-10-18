# 08 Templates and Polymorphism

Templates reuse code across concrete types at compile time. Virtual interfaces let code call behavior selected by an object's runtime type.

## Constrain a Generic Function

```cpp
#include <concepts>
#include <iostream>
#include <string>

template <std::integral T>
T larger(T first, T second) {
    return first < second ? second : first;
}

class Labeler {
public:
    virtual ~Labeler() = default;
    virtual std::string label() const = 0;
};

class Book final : public Labeler {
public:
    std::string label() const override {
        return "Systems notes";
    }
};

void print_label(const Labeler& item) {
    std::cout << item.label() << '\n';
}

int main() {
    std::cout << larger(120, 310) << '\n';
    Book book;
    print_label(book);
}
```

`T` is deduced from the arguments. The `std::integral` concept restricts permitted types, so a string call does not satisfy the template. Both arguments here must deduce the same `T`. Concepts express requirements; they do not validate runtime values.

Template definitions usually need to be visible where instantiation occurs, so generic libraries commonly put their definitions in headers. Explicit instantiation is a more advanced alternative.

## Virtual Interfaces

`= 0` declares a pure virtual function, making `Labeler` abstract. `Book` implements it, and `override` asks the compiler to check the intended override. Passing a base reference preserves virtual dispatch; passing a derived object by base value can slice away its derived portion when the base is concrete.

A public virtual destructor supports safe deletion through a base pointer. Ownership still belongs in a value or smart pointer; virtual dispatch alone does not manage lifetime. Use templates for algorithms parameterized over types, and a virtual interface when runtime substitution is the actual requirement. Prefer simple concrete types when neither abstraction is needed.

[Next: Algorithms and Lambdas](09-algorithms-and-lambdas.md)

## References

- [C++ Core Guidelines: Templates and generic programming](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-templates)
- [C++ Core Guidelines: Class hierarchies](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#SS-hier)
- [C++ working draft: Integral concepts](https://eel.is/c++draft/concepts.arithmetic)
