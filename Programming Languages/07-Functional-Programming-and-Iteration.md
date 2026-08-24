# 07 Functional Programming and Iteration

## Table of Contents

1. [Overview](#overview)
2. [First-Class Functions](#first-class-functions)
3. [Closures](#closures)
4. [Iterators and Generators](#iterators-and-generators)
5. [Transformation Pipelines](#transformation-pipelines)
6. [Purity and Side Effects](#purity-and-side-effects)
7. [Concept Mapping](#concept-mapping)
8. [References](#references)

## Overview

Functional programming treats computation as the composition of functions and favors explicit data transformations over scattered mutation. Rust, Go, Python, and C++ are multi-paradigm languages: none requires a purely functional style, but all support first-class behavior and iteration abstractions to different degrees.

## First-Class Functions

A function is **first-class** when it can be stored, passed as an argument, and returned as a value. A higher-order function consumes or produces another function.

~~~rust
fn apply_twice(value: i32, operation: fn(i32) -> i32) -> i32 {
    operation(operation(value))
}
~~~

~~~go
func ApplyTwice(value int, operation func(int) int) int {
    return operation(operation(value))
}
~~~

~~~python
from collections.abc import Callable

def apply_twice(value: int, operation: Callable[[int], int]) -> int:
    return operation(operation(value))
~~~

~~~cpp
template<class F>
int apply_twice(int value, F operation) {
    return operation(operation(value));
}
~~~

## Closures

A closure is a function value that captures names from its surrounding scope. Capture semantics matter because the closure may copy a value, borrow it, share it, or outlive the call that created it.

~~~rust
let minimum = 10;
let accepted: Vec<_> = values.into_iter()
    .filter(|value| *value >= minimum)
    .collect();
~~~

~~~go
minimum := 10
accepted := slices.DeleteFunc(values, func(value int) bool {
    return value < minimum
})
~~~

~~~python
minimum = 10
accepted = [value for value in values if value >= minimum]
~~~

~~~cpp
int minimum = 10;
std::vector<int> accepted;
std::ranges::copy_if(values, std::back_inserter(accepted),
                     [minimum](int value) { return value >= minimum; });
~~~

Rust closure traits (`Fn`, `FnMut`, and `FnOnce`) describe how captured state is used. C++ capture lists state whether names are captured by value or reference. Go and Python capture variables through their language's normal closure rules; take care when a closure observes a loop variable that later changes.

## Iterators and Generators

An iterator produces a sequence one item at a time. This separates traversal from storage and can avoid constructing intermediate collections.

Rust iterators are lazy until consumed by operations such as `collect`, `sum`, or a loop. Python iterators and generator expressions are also lazy. C++ ranges often create lazy views. Go's core language traditionally emphasizes loops; iterator functions and library helpers can provide similar pull- or push-based abstractions, but explicit loops remain idiomatic.

Python generators suspend a function at `yield` and resume it to produce the next item:

~~~python
def countdown(start: int):
    while start > 0:
        yield start
        start -= 1
~~~

Laziness saves work only if consumers do not need every result. It also changes when errors and side effects occur, so document whether a returned sequence has already performed its work.

## Transformation Pipelines

Common operations include:

- **map:** transform each item;
- **filter:** retain items satisfying a predicate;
- **fold/reduce:** combine items into one result;
- **flat-map:** transform each item into zero or more items and flatten the result;
- **take/limit:** consume only an initial part of a sequence.

For a short stateful algorithm, a normal loop may be clearer than a dense pipeline. Prefer the form that makes data flow, early exit, and failure behavior easiest to see.

## Purity and Side Effects

A pure function depends only on its arguments and produces no externally visible side effects. Pure code is easier to test and compose, but useful programs must eventually perform I/O, update state, or communicate.

Keep effects near explicit boundaries. Avoid hiding network calls, mutation, or logging inside an operation that appears to be a simple transformation. When parallelizing a pipeline, functions that mutate captured shared state require synchronization and may make results order-dependent.

## Concept Mapping

| Concept | Rust | Go | Python | C++ |
|---|---|---|---|---|
| Anonymous function | closure `|x| ...` | function literal | `lambda` or nested function | lambda `[capture](...) { ... }` |
| Lazy sequence | `Iterator` | iterator function or explicit loop | iterator/generator | ranges view |
| Transform | `.map(...)` | loop or library helper | `map` or comprehension | `views::transform` |
| Select | `.filter(...)` | loop or library helper | `filter` or comprehension | `views::filter` |
| Consume/combine | `collect`, `fold`, `sum` | loop | collection, `sum`, `functools.reduce` | range algorithm or `accumulate` |

## References

- [The Rust Book — Closures and Iterators](https://doc.rust-lang.org/book/ch13-00-functional-features.html)
- [Go Language Specification — Function literals](https://go.dev/ref/spec#Function_literals)
- [Python Functional Programming HOWTO](https://docs.python.org/3/howto/functional.html)
- [C++ working draft — Lambda expressions](https://eel.is/c++draft/expr.prim.lambda)
