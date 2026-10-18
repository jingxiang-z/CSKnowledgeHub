# 09 Algorithms and Lambdas

Standard algorithms express common traversal operations. Lambdas provide small callable objects that can capture local values for predicates and transformations.

## Filter, Order, and Aggregate

```cpp
#include <algorithm>
#include <iostream>
#include <iterator>
#include <numeric>
#include <vector>

int main() {
    const std::vector<int> scores{91, 62, 75, 44};
    const int threshold = 75;
    std::vector<int> passing;

    std::copy_if(scores.begin(), scores.end(), std::back_inserter(passing),
                 [threshold](int score) { return score >= threshold; });
    std::ranges::sort(passing);

    const int total = std::accumulate(passing.begin(), passing.end(), 0);
    for (int score : passing) {
        std::cout << score << '\n';
    }
    std::cout << "Total: " << total << '\n';
}
```

The iterator pair `[begin, end)` describes a half-open range: `end` is a boundary, not an element to dereference. `std::back_inserter` turns output assignments into `push_back` calls. It lets the destination grow; writing into `passing.begin()` while it is empty would not create storage.

## Captures and Lifetime

`[threshold]` captures a copy of that value. `[&threshold]` captures access by reference, which requires the original to remain alive while the closure uses it. `[=]` and `[&]` give default capture modes, but explicit captures make dependencies easier to review.

A lambda stored or returned from a function must not retain references to locals that have been destroyed. Capturing a pointer copies the pointer, not the object it addresses, so the pointed-to object's lifetime still matters.

## Ranges and Eager Algorithms

`std::ranges::sort` accepts the whole container. Other C++20 range facilities can compose lazy views, but those views often borrow their sources and retain iterators. In contrast, `copy_if` above executes immediately and builds an independent vector of integers.

Algorithms have requirements: sorting needs suitable random-access traversal, and a comparator must define a strict weak ordering. Do not mutate a source in a way that invalidates traversal while an algorithm is using it. `accumulate` uses its initial value's type for the accumulator, so choose that type for the expected numeric range.

[Next: Tests and Tooling](10-tests-and-tooling.md)

## References

- [C++ Core Guidelines: Standard library algorithms](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#SS-algo)
- [C++ working draft: Algorithms library](https://eel.is/c++draft/algorithms)
- [C++ working draft: Lambda expressions](https://eel.is/c++draft/expr.prim.lambda)
