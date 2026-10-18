# 10 Tests and Tooling

Compiler checks catch many type errors, but behavioral tests and runtime diagnostics address different failure modes. Keep small checks easy to compile and run.

## Check Boundary Behavior

Save this standalone example as `test_titles.cpp`:

```cpp
#include <iostream>
#include <stdexcept>
#include <string>
#include <string_view>

std::string require_title(std::string_view title) {
    if (title.empty()) {
        throw std::invalid_argument("Title must not be empty");
    }
    return std::string{title};
}

int main() {
    if (require_title("Systems notes") != "Systems notes") {
        std::cerr << "Valid title was not preserved\n";
        return 1;
    }

    bool rejected = false;
    try {
        (void)require_title("");
    } catch (const std::invalid_argument&) {
        rejected = true;
    }
    if (!rejected) {
        std::cerr << "Empty title was accepted\n";
        return 1;
    }

    std::cout << "All title checks passed\n";
}
```

The process returns nonzero when a check fails. These explicit checks remain active in release builds. The standard `assert` macro is useful for internal assumptions but can be disabled with `NDEBUG`; do not rely on it for external input validation or always-on test checks.

## Warnings and Sanitizers

With a GCC installation supporting these sanitizers:

```sh
g++ -std=c++20 -Wall -Wextra -Wpedantic -g -O1 -fsanitize=address,undefined -fno-omit-frame-pointer test_titles.cpp -o title-tests
./title-tests
```

AddressSanitizer detects many memory access mistakes; UndefinedBehaviorSanitizer checks selected undefined operations. They diagnose exercised paths, not all possible executions. A clean run does not prove a program correct. Use a debugger such as GDB or LLDB to inspect failures, and test expected failures as well as successful operations.

## Larger Projects

A build system can track source dependencies, compiler options, and test executables. CMake with CTest is one common choice; follow the repository's existing build configuration when present. A testing framework becomes useful when richer assertions, fixtures, and reporting justify it. Formatting and static analysis should also follow project configuration.

Return to the [C++ learning path](README.md).

## References

- [GCC: Warning options](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html)
- [GCC: Instrumentation options](https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html)
- [CMake: CTest](https://cmake.org/cmake/help/latest/manual/ctest.1.html)
