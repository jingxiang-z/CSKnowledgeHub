# 09 Testing, Debugging, and Tooling

## Table of Contents

1. [Overview](#overview)
2. [Automated Tests](#automated-tests)
3. [Test Design](#test-design)
4. [Diagnostics and Debugging](#diagnostics-and-debugging)
5. [Formatting and Static Analysis](#formatting-and-static-analysis)
6. [Profiling and Benchmarking](#profiling-and-benchmarking)
7. [Concept Mapping](#concept-mapping)
8. [References](#references)

## Overview

Tooling turns source code into evidence. Tests check specified behavior, compilers and linters identify suspicious code, debuggers reveal runtime state, and profilers show where time and memory are actually spent. These tools complement one another; passing tests do not prove the absence of defects, and a clean linter report does not prove correct behavior.

## Automated Tests

### Rust

Rust has built-in test attributes and a Cargo test runner. Unit tests often live beside the code; integration tests live under `tests/`.

~~~rust
fn add(left: i32, right: i32) -> i32 {
    left + right
}

#[test]
fn adds_negative_values() {
    assert_eq!(add(-2, 5), 3);
}
~~~

Run all tests with `cargo test`.

### Go

Go tests use functions named `TestXxx` in `_test.go` files. Table-driven tests compactly express multiple cases.

~~~go
func TestAdd(t *testing.T) {
    if got := Add(-2, 5); got != 3 {
        t.Fatalf("Add(-2, 5) = %d; want 3", got)
    }
}
~~~

Run them with `go test ./...`; add `-race` when exercising concurrent code.

### Python

Python includes `unittest`; projects also commonly use compatible third-party test runners. Keep test assertions focused on observable behavior.

~~~python
import unittest

class AddTests(unittest.TestCase):
    def test_adds_negative_values(self) -> None:
        self.assertEqual(add(-2, 5), 3)
~~~

Run standard-library tests with `python -m unittest`.

### C++

C++ does not prescribe one test framework. A project may use a framework integrated with its build system, or start with assertions for small internal checks.

~~~cpp
void test_adds_negative_values() {
    assert(add(-2, 5) == 3);
}
~~~

Use the project's test runner, often exposed through CTest, so local and continuous-integration commands match.

## Test Design

A useful test states the behavior being protected and fails for one understandable reason.

- Test normal cases, boundaries, empty input, invalid input, and failure cleanup.
- Test public behavior rather than private implementation details.
- Make tests deterministic: control clocks, random seeds, environment, and external services.
- Use fakes at slow or unreliable boundaries, but keep integration tests for the real boundary contract.
- Add a regression test before or with a bug fix so the defect cannot silently return.
- Use property-based or fuzz testing when broad input spaces and invariants matter.

The test pyramid is a heuristic, not a quota: many fast focused tests, fewer boundary/integration tests, and a small number of end-to-end tests usually give useful feedback without excessive runtime.

## Diagnostics and Debugging

Start with the smallest reproducible input. Read the complete diagnostic, including the first relevant error and its cause chain, before changing code.

A debugger can pause execution, inspect frames and variables, set conditional breakpoints, and watch state change. Rust and C++ commonly use GDB or LLDB; Go provides Delve; Python includes `pdb`. Logging is better for behavior that cannot easily be reproduced interactively, but logs should contain context without exposing secrets.

Assertions document and check internal invariants. They are not a substitute for validating untrusted input, and builds may disable some assertion mechanisms.

## Formatting and Static Analysis

Standard formatters remove style debates and produce stable diffs. Static analyzers inspect code without executing every path.

| Language | Formatter | Common checks |
|---|---|---|
| Rust | `rustfmt` | compiler warnings, Clippy |
| Go | `gofmt` | `go vet`, compiler, additional linters |
| Python | tool-dependent | type checker, linter, import/security checks |
| C++ | commonly `clang-format` | compiler warnings, `clang-tidy`, sanitizers |

Treat warnings consistently in continuous integration, but configure tools deliberately. A suppressed warning should include a reason when that reason is not obvious from the code.

## Profiling and Benchmarking

Optimize after measuring a representative workload. A profiler identifies where CPU time, allocations, blocking, or I/O waits occur. A benchmark compares a defined operation under controlled conditions.

Warm-up, compiler optimization, input distribution, caching, and system load can distort results. Report the environment and compare multiple runs. Improve the dominant bottleneck, then measure again; microbenchmark gains may not improve end-to-end latency.

Memory-safety tools are especially important for C++: use AddressSanitizer and UndefinedBehaviorSanitizer where supported. Thread sanitizers and race detectors help across concurrent native-code projects, though tool support varies by platform and language runtime.

## Concept Mapping

| Purpose | Rust | Go | Python | C++ |
|---|---|---|---|---|
| Built-in test support | `#[test]`, `cargo test` | `testing`, `go test` | `unittest` | no single language-standard runner |
| Interactive debugger | GDB / LLDB | Delve | `pdb` | GDB / LLDB / platform debugger |
| Standard formatter | `rustfmt` | `gofmt` | tool-dependent | tool-dependent, often `clang-format` |
| Static analysis | compiler / Clippy | compiler / `go vet` | type checkers / linters | warnings / `clang-tidy` |
| Benchmark/profile | Cargo ecosystem tools | `testing.B`, `pprof` | `timeit`, `cProfile`, ecosystem tools | framework and platform tools |

## References

- [The Rust Book — Writing Automated Tests](https://doc.rust-lang.org/book/ch11-00-testing.html)
- [Go documentation — Testing package](https://pkg.go.dev/testing)
- [Python documentation — Development Tools](https://docs.python.org/3/library/development.html)
- [CMake documentation — Testing with CTest](https://cmake.org/cmake/help/latest/guide/tutorial/Testing%20and%20CTest.html)
