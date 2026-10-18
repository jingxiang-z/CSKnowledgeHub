# Rust Essentials

Learn enough Rust to read and extend the foundation examples. These ten short chapters follow the topic order of [The Rust Programming Language](https://doc.rust-lang.org/book/), combining setup with basic syntax and keeping only the core concepts needed for small programs.

## Learning Path

| Chapter | What you will learn | Rust Book chapters |
|---|---|---|
| [01 Getting Started and Common Concepts](01-getting-started-and-common-concepts.md) | Cargo, variables, types, functions, and control flow | 1, 3 |
| [02 Ownership, References, and Slices](02-ownership-references-and-slices.md) | moves, borrowing, mutation, and borrowed views | 4 |
| [03 Structs and Methods](03-structs-and-methods.md) | named fields, constructors, privacy, and methods | 5 |
| [04 Enums and Pattern Matching](04-enums-and-pattern-matching.md) | variants, `Option`, `match`, and `if let` | 6 |
| [05 Packages, Crates, and Modules](05-packages-crates-and-modules.md) | file layout, paths, visibility, and dependencies | 7 |
| [06 Common Collections](06-common-collections.md) | `Vec`, `String`, and `HashMap` | 8 |
| [07 Error Handling](07-error-handling.md) | `Result`, propagation with `?`, and panic | 9 |
| [08 Generics, Traits, and Lifetimes](08-generics-traits-and-lifetimes.md) | reusable types, shared behavior, and borrow relationships | 10 |
| [09 Tests and Tooling](09-tests-and-tooling.md) | unit tests, integration tests, formatting, and linting | 11, Appendix D |
| [10 Closures and Iterators](10-closures-and-iterators.md) | captures, lazy adapters, and consuming iterators | 13 |

Read in order the first time. Each chapter has a small example. Rust code blocks are standalone programs unless the text gives a Cargo file layout.

## Scope and Further Reading

Smart pointers, concurrency, async, advanced traits, macros, and unsafe Rust can wait until a project needs them; use the Rust Book for those topics. The introductory patterns here cover ordinary `match` usage without a separate patterns chapter.

Return to [Programming Language Foundations](../README.md) for the other language guides.

## References

- [The Rust Programming Language](https://doc.rust-lang.org/book/)
- [Rust standard library documentation](https://doc.rust-lang.org/std/)
