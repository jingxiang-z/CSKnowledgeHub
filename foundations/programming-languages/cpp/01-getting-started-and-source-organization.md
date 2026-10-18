# 01 Getting Started and Source Organization

A C++ compiler checks source files and produces object code. A linker combines that code and libraries into an executable. Headers commonly share declarations between source files.

## Compile a Small Program

Install a compiler with C++20 support. Save this as `main.cpp`:

```cpp
#include <iostream>

int main() {
    std::cout << "Systems notes\n";
}
```

Compile and run from the same directory:

```sh
g++ -std=c++20 -Wall -Wextra -Wpedantic -g main.cpp -o app
./app
```

`-std=c++20` selects the language version, warning flags enable diagnostics, and `-g` emits debugging information. `main` is the program entry point; reaching its end returns success. `#include <iostream>` makes the standard stream declarations available, and `std::` qualifies names in the standard namespace.

## Separate Declarations and Definitions

For a separate multi-file example, create these files in one directory.

`catalog.hpp`:

```cpp
#ifndef CATALOG_HPP
#define CATALOG_HPP

namespace catalog {
bool valid_pages(int pages);
}

#endif
```

`catalog.cpp`:

```cpp
#include "catalog.hpp"

namespace catalog {
bool valid_pages(int pages) {
    return pages > 0;
}
}
```

`main.cpp`:

```cpp
#include "catalog.hpp"
#include <iostream>

int main() {
    std::cout << catalog::valid_pages(310) << '\n';
}
```

Build with `g++ -std=c++20 -Wall -Wextra -Wpedantic main.cpp catalog.cpp -o app`. The declaration lets `main.cpp` call the function; `catalog.cpp` supplies its definition. Omitting that source file normally produces a link error.

The include guard prevents repeated inclusion of the header's contents in one translation unit. Do not include `.cpp` files to assemble ordinary projects. Keep non-inline function definitions in source files and include each required standard header directly. Templates commonly need definitions visible in headers, as chapter 8 explains.

[Next: Values, Functions, and Control Flow](02-values-functions-and-control-flow.md)

## References

- [GCC: Invoking G++](https://gcc.gnu.org/onlinedocs/gcc/Invoking-G_002b_002b.html)
- [C++ Core Guidelines: Source files](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-source)
