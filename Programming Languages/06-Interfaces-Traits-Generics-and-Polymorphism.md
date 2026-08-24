# 06 Interfaces, Traits, Generics, and Polymorphism

## Table of Contents

1. [Overview](#overview)
2. [Behavioral Abstraction](#behavioral-abstraction)
3. [Generic Programming](#generic-programming)
4. [Static and Dynamic Dispatch](#static-and-dynamic-dispatch)
5. [Design Guidelines](#design-guidelines)
6. [Concept Mapping](#concept-mapping)
7. [References](#references)

## Overview

Abstraction lets code depend on required behavior instead of a concrete representation. Traits, interfaces, protocols, abstract base classes, templates, and generic type parameters express that idea differently. **Polymorphism** means the same operation can work with values of multiple types.

## Behavioral Abstraction

### Rust

A trait names required behavior. Implementations are explicit, and a trait bound states what a generic function needs.

~~~rust
trait Summarize {
    fn summary(&self) -> String;
}

fn print_summary(item: &impl Summarize) {
    println!("{}", item.summary());
}
~~~

### Go

An interface is a method set. A type satisfies it implicitly by providing those methods; no declaration connects the type to the interface.

~~~go
type Summarizer interface {
    Summary() string
}

func PrintSummary(item Summarizer) {
    fmt.Println(item.Summary())
}
~~~

Prefer small interfaces defined near the code that consumes them.

### Python

Python commonly uses duck typing: a function accepts any object that supports the operations it performs. `typing.Protocol` makes that structural requirement visible to static type checkers without changing runtime behavior.

~~~python
from typing import Protocol

class Summarizer(Protocol):
    def summary(self) -> str: ...

def print_summary(item: Summarizer) -> None:
    print(item.summary())
~~~

Abstract base classes are useful when runtime registration, shared implementation, or explicit inheritance is required.

### C++

A class with virtual functions provides runtime polymorphism. A protected or virtual destructor is important when objects may be destroyed through a base pointer.

~~~cpp
class Summarizer {
public:
    virtual ~Summarizer() = default;
    virtual std::string summary() const = 0;
};

void print_summary(const Summarizer& item) {
    std::cout << item.summary() << '\n';
}
~~~

C++20 concepts can instead describe compile-time requirements without requiring inheritance.

## Generic Programming

Generics describe an algorithm or container once while preserving the concrete type of each use.

~~~rust
fn first<T>(items: &[T]) -> Option<&T> {
    items.first()
}
~~~

~~~go
func First[T any](items []T) (T, bool) {
    if len(items) == 0 {
        var zero T
        return zero, false
    }
    return items[0], true
}
~~~

~~~python
from typing import TypeVar

T = TypeVar("T")

def first(items: list[T]) -> T | None:
    return items[0] if items else None
~~~

~~~cpp
template<class T>
const T* first(const std::vector<T>& items) {
    return items.empty() ? nullptr : &items.front();
}
~~~

A type parameter should express a relationship that matters. For example, returning the same `T` passed by a caller conveys more information than accepting and returning an unconstrained top type such as Python's `object` or Go's `any`.

Bounds or constraints state the capabilities an implementation uses. Avoid adding operations “just in case”; narrower constraints admit more types and reduce coupling.

## Static and Dynamic Dispatch

With **static dispatch**, the concrete operation is selected during compilation, commonly through Rust generics or `impl Trait`, Go generic instantiation, and C++ templates. It often enables inlining and stores no runtime method table, but can increase generated code size.

With **dynamic dispatch**, the concrete operation is selected at runtime through a Rust trait object, Go interface value, Python attribute lookup, or C++ virtual function. It supports heterogeneous collections and runtime substitution, with some runtime indirection and fewer compile-time optimization opportunities.

Choose based on the required flexibility. Performance differences should be measured rather than assumed.

## Design Guidelines

- Depend on the smallest behavior the consumer needs.
- Use generics when types vary but the algorithm and result relationships stay the same.
- Use dynamic dispatch when concrete types must vary at runtime or be stored together.
- Prefer composition and capability-based interfaces to deep inheritance hierarchies.
- Keep domain invariants in concrete types; an interface should not expose representation details.
- Avoid a “universal” interface whose methods unrelated implementations cannot meaningfully support.

## Concept Mapping

| Concept | Rust | Go | Python | C++ |
|---|---|---|---|---|
| Behavioral contract | trait | interface | protocol, ABC, or duck typing | abstract base class or concept |
| Generic function | `<T>` with bounds | `[T constraint]` | `TypeVar` / modern type-parameter syntax | template |
| Conformance | explicit `impl` | implicit method-set match | structural or inherited | inheritance or constraint satisfaction |
| Static dispatch | generic / `impl Trait` | generic | limited; runtime execution remains dynamic | template / concept |
| Dynamic dispatch | `dyn Trait` | interface value | normal method lookup | virtual function |

## References

- [The Rust Book — Traits](https://doc.rust-lang.org/book/ch10-02-traits.html)
- [Go Language Specification — Interface types](https://go.dev/ref/spec#Interface_types)
- [Python typing — Protocols](https://typing.python.org/en/latest/spec/protocol.html)
- [C++ working draft — Constraints and concepts](https://eel.is/c++draft/temp.constr)
