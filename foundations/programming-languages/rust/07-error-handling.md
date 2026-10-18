# 07 Error Handling

Use `Result<T, E>` when an operation can fail with an explanation. Return `Ok(value)` on success or `Err(error)` on failure, and let the caller decide how to respond.

## Validate and Propagate

```rust
fn parse_pages(input: &str) -> Result<u32, &'static str> {
    let pages = input.parse::<u32>().map_err(|_| "Expected a nonnegative integer")?;
    if pages == 0 {
        return Err("Page count must be positive");
    }
    Ok(pages)
}

fn describe(input: &str) -> Result<String, &'static str> {
    let pages = parse_pages(input)?;
    Ok(format!("Book has {pages} pages"))
}

fn main() {
    for input in ["310", "zero", "0", "-1"] {
        match describe(input) {
            Ok(message) => println!("{message}"),
            Err(error) => eprintln!("{input:?}: {error}"),
        }
    }
}
```

For a `Result`, `?` extracts an `Ok` value or returns an error from the current function. The enclosing function must have a compatible return type. Error conversion uses `From` where applicable; `?` does not automatically turn arbitrary errors into strings.

`map_err` changes the error type before propagation. Here it deliberately reduces parse errors to one simple message. `&'static str` works because these messages are string literals valid for the whole program; structured error types are useful when callers need to distinguish failure cases.

## Option, Result, and Panic

| Outcome | Typical representation |
|---|---|
| A lookup has no matching item | `Option<T>` |
| Validation or an operation fails | `Result<T, E>` |
| Execution reaches an unrecoverable condition or violated assumption | `panic!` |

Convert an `Option` to a `Result` with `ok_or(error)` when missing data should be reported as failure. The library catalog uses this for missing books.

`unwrap()` and `expect()` panic on `Err` or `None`; `expect()` adds context. Avoid them for routine invalid input. A `u32` prevents representing a negative page count after parsing, but textual input still needs parsing and validation.

[Next: Generics, Traits, and Lifetimes](08-generics-traits-and-lifetimes.md)

## References

- [Rust Book: Error Handling](https://doc.rust-lang.org/book/ch09-00-error-handling.html)
