# Go Essentials

Learn enough Go to read and extend the foundation examples. These ten short chapters follow the progression of [A Tour of Go](https://go.dev/tour/list), with practical additions from the [official documentation](https://go.dev/doc/). Each chapter includes an example and official references.

## Learning Path

| Chapter | What you will learn | Official starting point |
|---|---|---|
| [01 Getting Started, Packages, and Modules](01-getting-started-packages-and-modules.md) | toolchain, project layout, imports, and visibility | Getting started; module layout |
| [02 Values, Functions, and Control Flow](02-values-functions-and-control-flow.md) | types, declarations, multiple returns, loops, and branches | Tour: basics and flow control |
| [03 Pointers, Structs, and Methods](03-pointers-structs-and-methods.md) | copying, shared access, receivers, and composition | Tour: more types and methods |
| [04 Collections and Text](04-collections-and-text.md) | arrays, slices, maps, and UTF-8 strings | Tour: more types |
| [05 Functions and Interfaces](05-functions-and-interfaces.md) | closures, implicit implementation, and interface values | Tour: function values and interfaces |
| [06 Errors and Deferred Cleanup](06-errors-and-deferred-cleanup.md) | error returns, wrapping, inspection, and cleanup | Tour: errors and defer; standard library |
| [07 Generics](07-generics.md) | type parameters, constraints, and reusable operations | Tour: generics; generics tutorial |
| [08 Goroutines and Channels](08-goroutines-and-channels.md) | concurrent execution, communication, closing, and select | Tour: concurrency |
| [09 Synchronization and Cancellation](09-synchronization-and-cancellation.md) | mutexes, joining work, contexts, and goroutine lifetime | Tour: mutexes; sync and context docs |
| [10 Tests and Tooling](10-tests-and-tooling.md) | table tests, formatting, vet, and race detection | Testing tutorial; Go command docs |

Read in order the first time. Go code blocks are standalone programs unless the text specifies a file layout. Use a separate practice module so experiments do not change the repository's examples.

## Scope and Further Reading

This path covers the language and tools needed for small programs. Web frameworks, reflection, unsafe code, advanced concurrency designs, and publishing modules can wait until a project needs them. Use [Effective Go](https://go.dev/doc/effective_go) for additional idioms, alongside the current modules and generics documentation; it does not cover all modern Go features.

Return to [Programming Language Foundations](../README.md) for the other language guides.

## References

- [A Tour of Go](https://go.dev/tour/list)
- [Official Go documentation](https://go.dev/doc/)
- [Go standard library](https://pkg.go.dev/std)
