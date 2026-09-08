# Programming Language Foundations

This section provides the language foundations needed to understand systems code. It focuses on data modeling, memory and resource lifetimes, error handling, concurrency, and tooling. The examples explain semantic differences without requiring readers to master Python, Go, C++, and Rust at the same time.

## Learning Path

| Chapter | Focus |
|---|---|
| [01 Basic Programming Concepts](01-basic-programming-concepts.md) | variables, types, collections, functions, control flow, and comments |
| [02 Data Modeling: Structs and Classes](02-data-modeling-structs-and-classes.md) | custom types, methods, invariants, composition, and inheritance |
| [03 Memory, Ownership, and References](03-memory-ownership-and-references.md) | lifetime, cleanup, copying, moving, aliasing, and views |
| [04 Code Organization, Packages, and Dependencies](04-code-organization-packages-and-dependencies.md) | modules, public APIs, packages, workspaces, and releases |
| [05 Error Handling and Recovery](05-error-handling-and-recovery.md) | expected failures, propagation, exceptions, cleanup, and panic |
| [06 Interfaces, Traits, Generics, and Polymorphism](06-interfaces-traits-generics-and-polymorphism.md) | reusable abstractions, type parameters, bounds, and dispatch |
| [07 Functional Programming and Iteration](07-functional-programming-and-iteration.md) | first-class functions, closures, iterators, generators, and laziness |
| [08 Concurrency and Asynchronous Programming](08-concurrency-and-asynchronous-programming.md) | threads, tasks, channels, shared state, futures, and cancellation |
| [09 Testing, Debugging, and Tooling](09-testing-debugging-and-tooling.md) | automated tests, diagnostics, formatting, debugging, and profiling |
| [10 Type Systems and Language Semantics](10-type-systems-and-language-semantics.md) | type checking, type relationships, variants, nullability, and evaluation |

## Practice

Foundational examples are in [examples](examples/) and practice types, data modeling, state transitions, and error handling. Larger systems exercises are in the [Lab index](../../labs/README.md), starting with Python and Go implementations and adding C++ and Rust later as needed.

## Scope

These notes emphasize practical language concepts rather than compiler construction. Parsing, abstract syntax trees, interpreters, compiler passes, and formal operational semantics are natural follow-on topics, but are outside the current learning path.
