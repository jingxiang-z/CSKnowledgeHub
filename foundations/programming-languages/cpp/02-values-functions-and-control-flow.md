# 02 Values, Functions, and Control Flow

C++ uses static types and supports both value copying and reference parameters. Initialize local values explicitly and use ordinary control flow to make operations clear.

## Initialize and Traverse

```cpp
#include <array>
#include <iostream>

bool passes(int score, int threshold = 75) {
    return score >= threshold;
}

int main() {
    constexpr int threshold = 75;
    const std::array<int, 3> scores{72, 88, 95};
    int total{};
    int passed{};

    for (int score : scores) {
        total += score;
        if (passes(score, threshold)) {
            ++passed;
        }
    }

    const double average = static_cast<double>(total) / scores.size();
    std::cout << passed << " passes, average " << average << '\n';
}
```

`int total{}` initializes to zero. Brace initialization rejects many narrowing conversions, such as placing a floating-point value into an integer. `const` prevents modification through that object or access path. `constexpr` declares a value usable in constant expressions when its requirements are satisfied.

`auto` deduces a static type from an initializer; it does not make a variable dynamically typed. Fundamental types include integers, floating-point types, `bool`, and character types. Integer widths depend on the type and implementation; use fixed-width types from `<cstdint>` when a representation requires them.

## Functions and Branches

`passes` takes integer values by copy and returns a boolean. Function overloads can share a name with different parameter lists; the compiler selects a match. Default arguments supply omitted values at the call site.

Use `if`/`else` for conditions, `switch` for discrete cases, and `for` or `while` for repetition. A `switch` case can fall through unless it exits, commonly with `break`. Prefer range-based `for` for container traversal. `&&` and `||` short-circuit evaluation.

Integer division truncates toward zero, so the example converts before division. Signed integer overflow is undefined behavior; unsigned arithmetic wraps modulo its range. Choose types and validation based on the actual input bounds, rather than assuming all arithmetic is safe.

[Next: Structs, Classes, and Methods](03-structs-classes-and-methods.md)

## References

- [C++ Core Guidelines: Expressions and statements](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-expr)
- [C++ Core Guidelines: Functions](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-functions)
