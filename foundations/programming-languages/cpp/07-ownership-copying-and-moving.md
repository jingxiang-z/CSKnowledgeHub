# 07 Ownership, Copying, and Moving

Value semantics make ordinary copies independent when a type owns its contents. Moves can transfer resources, and smart pointers represent explicit dynamic ownership.

## Transfer Responsibility

```cpp
#include <iostream>
#include <memory>
#include <string>
#include <utility>

struct Book {
    std::string title;
};

int main() {
    std::string original{"Systems notes"};
    std::string copied = original;
    copied += " copy";

    std::string moved = std::move(original);
    original = "Reused source";
    std::cout << original << " / " << copied << " / " << moved << '\n';

    auto owner = std::make_unique<Book>(Book{"Python notes"});
    const Book* borrowed = owner.get();
    std::cout << borrowed->title << '\n';

    auto next_owner = std::move(owner);
    std::cout << std::boolalpha << (owner == nullptr) << '\n';
    std::cout << next_owner->title << '\n';
}
```

Copying `std::string` copies its value. A copy of a container holding pointers still shares the pointed-to objects; value copying does not automatically deep-copy an arbitrary object graph.

`std::move` is a cast that makes move operations eligible; it does not itself transfer resources. The destination type's selected operation performs the work, and some types may copy instead. A moved-from standard string remains valid but its contents are unspecified; assigning a fresh value is safe.

## Smart Pointer Choices

`std::unique_ptr<T>` owns one object exclusively, cannot be copied, and releases the object automatically. Moving it transfers ownership and leaves the source empty. A raw pointer obtained with `get()` borrows access; it does not participate in ownership or extend the object's lifetime.

Use `std::shared_ptr<T>` only when shared lifetime ownership is needed. It uses reference counting, and cycles can prevent cleanup; `std::weak_ptr<T>` observes shared ownership without keeping an object alive. Shared ownership does not make concurrent mutation of the object safe.

## Let Members Manage Resources

Prefer ordinary values before dynamic allocation. Compose standard owners such as strings, vectors, and smart pointers so their generated cleanup and copy/move behavior do the work. This is commonly called the Rule of Zero. A custom low-level owner requires deliberate destructor and copy/move design; avoid adding one for these examples.

[Next: Templates and Polymorphism](08-templates-and-polymorphism.md)

## References

- [C++ Core Guidelines: Resource management](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-resource)
- [C++ Core Guidelines: Copy and move](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#SS-copy)
- [C++ working draft: Unique ownership pointers](https://eel.is/c++draft/unique.ptr)
