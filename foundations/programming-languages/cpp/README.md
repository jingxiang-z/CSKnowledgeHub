# C++ Essentials

Learn the C++ needed to read and extend the foundation examples. These ten short chapters use a C++20 baseline and emphasize value types, standard containers, explicit lifetimes, and automatic resource management. Each chapter includes an example and references to the C++ Core Guidelines or the standard working draft.

## Learning Path

| Chapter | What you will learn |
|---|---|
| [01 Getting Started and Source Organization](01-getting-started-and-source-organization.md) | compilation, headers, source files, namespaces, and linking |
| [02 Values, Functions, and Control Flow](02-values-functions-and-control-flow.md) | initialization, types, parameters, branches, and loops |
| [03 Structs, Classes, and Methods](03-structs-classes-and-methods.md) | constructors, access control, invariants, and const methods |
| [04 Lifetimes, References, and RAII](04-lifetimes-references-and-raii.md) | scope, borrowing, pointers, and deterministic cleanup |
| [05 Containers, Strings, and Views](05-containers-strings-and-views.md) | vector, maps, string, span, and invalidation |
| [06 Errors and Optional Values](06-errors-and-optional-values.md) | exceptions, optional results, and validation |
| [07 Ownership, Copying, and Moving](07-ownership-copying-and-moving.md) | value semantics, smart pointers, and move operations |
| [08 Templates and Polymorphism](08-templates-and-polymorphism.md) | generic functions, concepts, and virtual interfaces |
| [09 Algorithms and Lambdas](09-algorithms-and-lambdas.md) | standard algorithms, captures, iterators, and ranges |
| [10 Tests and Tooling](10-tests-and-tooling.md) | behavioral checks, compiler warnings, sanitizers, and builds |

Read in order the first time. C++ code blocks are standalone programs unless file names indicate a multi-file layout. Commands use GCC on a POSIX shell; adapt compiler and executable names for your platform. Examples require no third-party libraries.

## Scope and Further Reading

Concurrency, coroutines, custom allocators, template metaprogramming, and C++ modules can wait until a project needs them. The working draft is a detailed reference, not a beginner tutorial, and may include features newer than this path's C++20 baseline. The Core Guidelines provide design guidance rather than a complete language specification.

Return to [Programming Language Foundations](../README.md) for the other language guides.

## References

- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
- [C++ standard working draft](https://eel.is/c++draft/)
- [GCC: Invoking G++](https://gcc.gnu.org/onlinedocs/gcc/Invoking-G_002b_002b.html)
