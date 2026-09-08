# 05 Error Handling and Recovery

## Table of Contents

1. [Overview](#overview)
2. [Expected and Unexpected Failure](#expected-and-unexpected-failure)
3. [Representing Failure](#representing-failure)
4. [Propagation and Context](#propagation-and-context)
5. [Cleanup](#cleanup)
6. [Designing Error Boundaries](#designing-error-boundaries)
7. [Concept Mapping](#concept-mapping)
8. [References](#references)

## Overview

Failure is part of a program's interface. A missing file, invalid input, or unavailable service is an expected possibility that callers may need to handle. A broken invariant or impossible state usually indicates a programming defect. Good error handling distinguishes these cases, preserves useful context, and releases resources on every path.

## Expected and Unexpected Failure

Use ordinary error values or exceptions for conditions a caller can reasonably anticipate. Reserve assertions, panics, and process termination for violated invariants or situations where the current component cannot continue safely.

Do not merely log an error and continue with an invalid value. Either recover locally, return the failure to a caller that can decide, or terminate at a well-defined application boundary.

## Representing Failure

### Rust

`Option<T>` represents a value that may be absent. `Result<T, E>` represents success or a recoverable failure and forces the caller to consider both cases.

~~~rust
fn parse_port(text: &str) -> Result<u16, String> {
    let port = text
        .parse::<u16>()
        .map_err(|error| format!("invalid port {text:?}: {error}"))?;

    if port == 0 {
        return Err("port must be greater than zero".to_string());
    }
    Ok(port)
}
~~~

Use `panic!`, `assert!`, or `expect` for violated assumptions, not routine invalid input.

### Go

Go functions conventionally return an `error` as their final result. A `nil` error means success. Callers check the error before using other results.

~~~go
func ParsePort(text string) (uint16, error) {
    value, err := strconv.ParseUint(text, 10, 16)
    if err != nil {
        return 0, fmt.Errorf("parse port %q: %w", text, err)
    }
    if value == 0 {
        return 0, errors.New("port must be greater than zero")
    }
    return uint16(value), nil
}
~~~

`panic` and `recover` exist, but ordinary application failures should normally remain errors.

### Python

Python reports failure with exceptions. Catch only exceptions the current layer can handle, and keep the protected `try` block narrow.

~~~python
def parse_port(text: str) -> int:
    try:
        port = int(text)
    except ValueError as error:
        raise ValueError(f"invalid port {text!r}") from error

    if not 1 <= port <= 65_535:
        raise ValueError("port must be between 1 and 65535")
    return port
~~~

Avoid a bare `except:` because it can hide interrupts, termination requests, and unrelated defects.

### C++

C++ can use exceptions, status values, `std::optional` for absence, and, since C++23, `std::expected` for an expected success-or-error result. The choice should be consistent at an API boundary.

~~~cpp
#include <charconv>
#include <expected>
#include <string>
#include <system_error>

std::expected<unsigned short, std::string> parse_port(std::string text) {
    unsigned int value = 0;
    auto [end, error] = std::from_chars(text.data(), text.data() + text.size(), value);
    if (error != std::errc{} || end != text.data() + text.size() ||
        value == 0 || value > 65535) {
        return std::unexpected("invalid port: " + text);
    }
    return static_cast<unsigned short>(value);
}
~~~

Exceptions are appropriate when the surrounding code follows exception-safe design. Never throw from a destructor during stack unwinding.

## Propagation and Context

Propagation lets a lower layer report failure to a layer with enough information to choose a response. Rust's `?`, an explicit Go `return`, Python's `raise`, and a C++ `throw` or returned `std::unexpected` serve this purpose.

Add context when crossing an abstraction boundary: “read configuration” is more useful than a bare “file not found.” Preserve the underlying cause where the language supports chaining or wrapping. Do not repeatedly log the same error at every layer; enrich it while propagating and normally log it once at the boundary that handles it.

## Cleanup

Error paths must release files, locks, sockets, and transactions.

| Language | Usual cleanup mechanism |
|---|---|
| Rust | ownership and `Drop`; guards release resources when scope ends |
| Go | `defer`, usually placed immediately after successful acquisition |
| Python | context managers and `with`; `finally` for general cleanup |
| C++ | RAII objects whose destructors release resources |

Cleanup should be deterministic for scarce external resources. Garbage collection manages memory reachability, but it is not a substitute for promptly closing a file or releasing a lock.

## Designing Error Boundaries

- Validate external data at the boundary where it enters the system.
- Use specific, stable error categories that callers can inspect without parsing messages.
- Translate low-level errors into domain-level errors when implementation details should remain private.
- Retry only transient, idempotent operations, with a limit and backoff.
- Preserve partial-failure rules: document whether an operation is atomic or may have changed state.
- Test failure paths, including cleanup and cancellation, rather than testing only success.

## Concept Mapping

| Purpose | Rust | Go | Python | C++ |
|---|---|---|---|---|
| Optional value | `Option<T>` | value plus `bool`, pointer, or domain type | `None` / `T | None` | `std::optional<T>` |
| Recoverable failure | `Result<T, E>` | final `error` result | exception | exception, status, or `std::expected<T, E>` |
| Propagate | `?` | explicit `if err != nil { return ... }` | `raise` | `throw` or return error |
| Add cause/context | error source or wrapper crate | `fmt.Errorf` with `%w` | `raise ... from ...` | nested exception or error object |
| Broken invariant | `panic!` / assertion | `panic` | assertion or unrecoverable exception | assertion, exception, or termination |

## References

- [The Rust Book — Recoverable Errors with Result](https://doc.rust-lang.org/book/ch09-02-recoverable-errors-with-result.html)
- [Go Blog — Working with Errors in Go 1.13](https://go.dev/blog/go1.13-errors)
- [Python Tutorial — Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html)
- [C++ working draft — Expected objects](https://eel.is/c++draft/expected)
