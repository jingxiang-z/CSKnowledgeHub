# 05 Containers, Strings, and Views

Use standard owning containers for storage and borrowed views for temporary access. The container's mutation rules determine which references and iterators remain valid.

## Store and Inspect Values

```cpp
#include <iostream>
#include <span>
#include <string>
#include <string_view>
#include <unordered_map>
#include <vector>

int sum(std::span<const int> values) {
    int total{};
    for (int value : values) {
        total += value;
    }
    return total;
}

int main() {
    std::vector<int> pages{120, 240, 310};
    std::cout << sum(pages) << '\n';

    std::unordered_map<std::string, int> counts;
    ++counts["Systems"];
    if (auto found = counts.find("Systems"); found != counts.end()) {
        std::cout << found->second << '\n';
    }

    std::string title{"Systems notes"};
    std::string_view view{title};
    std::cout << view.substr(0, 7) << '\n';
}
```

`std::vector<T>` owns a growable contiguous sequence. `std::array<T, N>` owns a fixed-size sequence. `std::unordered_map` provides hash-based lookup; `std::map` orders entries by key. In the example, `operator[]` inserts a missing key with a zero-initialized integer; `find` only looks it up.

## Checked Access and Invalidation

`vector.at(index)` throws on an out-of-range index. Under this C++20 baseline, out-of-bounds `operator[]` access has undefined behavior. Range-based loops avoid many indexing mistakes. `for (const auto& item : values)` reads without copying elements; `auto&` allows mutation.

Growing a vector can reallocate its storage and invalidate all pointers, references, spans, and iterators into its old storage. Erasure also invalidates affected access paths. Consult each container's operation-specific rules instead of assuming every view remains valid.

## Text and Borrowed Views

`std::string` owns character storage. `std::string_view` borrows characters and `std::span` borrows contiguous elements; neither extends the source's lifetime. Do not return a view into a temporary string or retain a view across an invalidating mutation.

`std::string` does not itself enforce UTF-8. For UTF-8 content, size and indexing work in bytes rather than Unicode code points. A substring of a string view may not be null-terminated, so its `data()` is not automatically a suitable C string.

[Next: Errors and Optional Values](06-errors-and-optional-values.md)

## References

- [C++ Core Guidelines: Standard library](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-stdlib)
- [C++ working draft: Vector modifiers](https://eel.is/c++draft/vector.modifiers)
- [C++ working draft: span](https://eel.is/c++draft/views.span)
- [C++ working draft: String views](https://eel.is/c++draft/string.view)
