# 10 Type Systems and Language Semantics

## Table of Contents

1. [Overview](#overview)
2. [Static and Dynamic Checking](#static-and-dynamic-checking)
3. [Nominal and Structural Relationships](#nominal-and-structural-relationships)
4. [Product and Sum Types](#product-and-sum-types)
5. [Nullability and Partial Operations](#nullability-and-partial-operations)
6. [Evaluation and Mutation](#evaluation-and-mutation)
7. [Exhaustiveness and Reachability](#exhaustiveness-and-reachability)
8. [Concept Mapping](#concept-mapping)
9. [References](#references)

## Overview

A type system classifies values and determines which operations are valid. Language semantics define what a program means: when expressions are evaluated, how names refer to values, what mutation changes, and what happens when execution encounters an error. Precise terminology helps explain differences that syntax alone can hide.

## Static and Dynamic Checking

Rust, Go, and C++ perform most type checking before execution. Python associates types with runtime objects; annotations support external static analysis but generally do not enforce types at runtime.

Static checking can reject whole categories of invalid programs before they run, but it cannot establish every domain rule. Dynamic checking permits highly flexible runtime behavior, but failures may appear only on an executed path. Neither approach makes validation of external data unnecessary.

“Strongly typed” and “weakly typed” have inconsistent definitions. Prefer concrete claims: whether implicit conversions occur, whether memory can be reinterpreted, and whether an invalid operation is rejected before execution or at runtime.

## Nominal and Structural Relationships

In a **nominal** relationship, compatibility depends on a declared name or relationship. In a **structural** relationship, compatibility depends on available members or operations.

- Rust trait implementation is explicit, while many ordinary types remain nominally distinct.
- Go interfaces are structural: a type satisfies an interface by having its method set.
- Python duck typing and protocols are structural; class inheritance is nominal.
- C++ class inheritance is nominal, while templates and concepts can accept types by their structure and operations.

Two types can have identical fields and still represent different domain concepts. Preserving that distinction can prevent accidentally mixing a user identifier with an order identifier.

## Product and Sum Types

A **product type** combines fields: a value contains a name *and* an address *and* a status. Structs, records, tuples, and classes commonly serve this role.

A **sum type** represents one of several alternatives: a payment is cash *or* card *or* bank transfer. Rust enums directly support tagged alternatives. C++ provides `std::variant`. Python can use unions of classes and pattern matching. Go commonly uses an interface with distinct implementations or a tagged struct whose tag and payload must be kept consistent.

~~~rust
enum Payment {
    Cash,
    Card { last_four: String },
    BankTransfer { reference: String },
}
~~~

Make invalid states hard to construct. A single record containing several unrelated nullable fields usually communicates alternatives less safely than a tagged representation.

## Nullability and Partial Operations

A partial operation is not valid for every input: indexing may be out of range, parsing may fail, and a search may find nothing. Its API should make that possibility visible.

- Rust commonly uses `Option<T>` or `Result<T, E>`.
- Go commonly returns a second `bool`, an `error`, or a pointer whose `nil` meaning is documented.
- Python commonly returns `None` for absence or raises an exception for failure; annotations can express `T | None`.
- C++ commonly uses `std::optional<T>`, `std::expected<T, E>`, an exception, or a documented iterator/sentinel.

Avoid sentinel data values such as `-1` when that value could later become valid or when the caller can easily forget to check it.

## Evaluation and Mutation

Most expressions in these languages evaluate eagerly: arguments are computed before a function body runs. Iterators, generators, ranges, futures, and short-circuit Boolean operators introduce delayed or conditional evaluation.

Names and assignment do not mean the same thing in every language:

- Rust assignment may move a non-`Copy` value, transferring ownership.
- Go assignment copies a value, although copied slices, maps, pointers, and interfaces may still refer to shared underlying data.
- Python assignment binds a name to an object; it does not copy that object.
- C++ assignment normally invokes value-specific copy or move behavior.

Mutation is observable through aliases that refer to the same state. This connects type semantics to the ownership, references, and views developed in chapter 03.

## Exhaustiveness and Reachability

An exhaustive branch handles every possible case. Rust checks exhaustive `match` expressions. Python pattern matching supports a wildcard case but static exhaustiveness depends on tooling and annotations. C++ visitation over `std::variant` can use overloaded callables, while completeness is expressed through whether every alternative is invocable. Go type switches often include a default case; adding a new interface implementation is not generally a closed-world compile-time event.

Exhaustiveness is most powerful with a closed set of variants. Extensible interface hierarchies instead make it easy to add a new type, but harder for a compiler to prove that a consumer considered every implementation. This is a design tradeoff, not a universal preference.

## Concept Mapping

| Question | Rust | Go | Python | C++ |
|---|---|---|---|---|
| Primary checking time | compile time | compile time | runtime; optional static analysis | compile time |
| Interface relationship | explicit trait implementation | structural method set | duck typing, protocol, or inheritance | inheritance, template, or concept |
| Direct sum type | `enum` | no direct closed sum type | union of types / class variants | `std::variant` or hierarchy |
| Absence | `Option<T>` | `nil`, value-plus-`bool`, or domain type | `None` | pointer or `std::optional<T>` |
| Assignment model | copy or move | value copy, sometimes sharing backing data | name binding | copy or move assignment |
| Exhaustive variant matching | compiler-checked `match` | generally manual | pattern matching; checker-dependent | visitor/overload completeness |

## References

- [The Rust Reference — Type System](https://doc.rust-lang.org/reference/type-system.html)
- [Go Language Specification — Types](https://go.dev/ref/spec#Types)
- [Python Language Reference — Data Model](https://docs.python.org/3/reference/datamodel.html)
- [C++ working draft — Basic concepts](https://eel.is/c++draft/basic)
