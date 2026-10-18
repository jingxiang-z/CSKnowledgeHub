# 04 Lifetimes, References, and RAII

An object must stay alive while code accesses it through a reference, pointer, or view. RAII ties resource cleanup to an owning object's lifetime, so ordinary scope exit releases its resources.

## Borrow Without Copying

```cpp
#include <iostream>
#include <string>

void append_note(std::string& title) {
    title += " updated";
}

void print_title(const std::string& title) {
    std::cout << title << '\n';
}

int main() {
    std::string title{"Systems notes"};
    const std::string& view = title;
    append_note(title);
    print_title(view);

    int pages{310};
    int* pointer = &pages;
    *pointer = 320;
    std::cout << pages << '\n';
}
```

`T&` refers to an existing object and allows mutation. `const T&` prevents modification through that reference, but does not make the original object immutable through all other paths. A reference must be initialized and cannot be reseated to another object.

`T*` is a pointer that can be reassigned or hold `nullptr`. `&object` obtains an address and `*pointer` accesses its referent. Raw pointers conventionally express borrowed access here; ownership belongs to values and smart pointers.

## Scope and Cleanup

Local automatic objects are destroyed when their scope ends, in reverse construction order. The destructor of a standard container releases its owned elements and storage. A file stream closes its associated file on destruction. This scope-based resource management also works during exception unwinding.

RAII means a resource-owning object acquires and releases responsibility through its construction and destruction. For small programs, using standard owning types usually provides this behavior without a custom destructor.

## Dangling Access

Never return a reference or pointer to a local object that will be destroyed on return. A stored reference does not generally keep its source alive. Returning a new `std::string` by value gives the caller ownership and is usually efficient.

C++ does not universally check these lifetime relationships. Container operations can also invalidate borrowed access, as the next chapter explains. Sanitizers can detect some mistakes when executed, but do not prove lifetime correctness.

[Next: Containers, Strings, and Views](05-containers-strings-and-views.md)

## References

- [C++ Core Guidelines: Resource management](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-resource)
- [C++ working draft: Object lifetime](https://eel.is/c++draft/basic.life)
