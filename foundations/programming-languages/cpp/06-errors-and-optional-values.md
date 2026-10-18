# 06 Errors and Optional Values

Use an optional value when absence is an ordinary result. Use exceptions when an operation cannot fulfill its contract and the caller needs to handle failure elsewhere.

## Parse Without Inventing a Sentinel

```cpp
#include <charconv>
#include <initializer_list>
#include <iostream>
#include <optional>
#include <stdexcept>
#include <string_view>
#include <system_error>

std::optional<int> parse_pages(std::string_view text) {
    if (text.empty()) {
        return std::nullopt;
    }
    int pages{};
    const auto [end, error] = std::from_chars(text.data(), text.data() + text.size(), pages);
    if (error != std::errc{} || end != text.data() + text.size() || pages <= 0) {
        return std::nullopt;
    }
    return pages;
}

int require_pages(std::string_view text) {
    if (auto pages = parse_pages(text)) {
        return *pages;
    }
    throw std::invalid_argument("Expected a positive page count");
}

int main() {
    for (std::string_view text : {"310", "zero", "0", "12x"}) {
        try {
            const int pages = require_pages(text);
            std::cout << pages << '\n';
        } catch (const std::invalid_argument& error) {
            std::cout << text << ": " << error.what() << '\n';
        }
    }
}
```

`std::optional<int>` contains an integer or no value, indicated by `std::nullopt`. Its boolean test checks presence before dereferencing. Calling `.value()` on an empty optional throws; dereferencing it without a value is invalid.

`from_chars` returns an end pointer and error code. Checking both rejects overflow and partially parsed text. This example intentionally accepts only positive integer text without whitespace or a leading plus sign.

## Exceptions and State

Catch exceptions by const reference to avoid copying and slicing. RAII destroys local owners during stack unwinding, so resources stay managed when a failure propagates. Validate before changing state when a failed operation should leave the object unchanged.

Do not use assertions for routine external input validation. `noexcept` promises that an exception will not escape a function; violating it terminates the program. Destructors should not let exceptions escape. C++23 adds `std::expected` for a value-or-error model, but it is outside this path's C++20 baseline.

[Next: Ownership, Copying, and Moving](07-ownership-copying-and-moving.md)

## References

- [C++ Core Guidelines: Error handling](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-errors)
- [C++ working draft: Optional objects](https://eel.is/c++draft/optional)
- [C++ working draft: from_chars](https://eel.is/c++draft/charconv.from.chars)
