# 09 Tests and Tooling

The compiler checks type and borrowing rules; tests check intended behavior. Keep tests focused on observable outcomes, including invalid input and boundary cases.

## Unit Tests

Put this example in the practice package's `src/lib.rs`:

```rust
pub fn validate_title(title: &str) -> Result<&str, &'static str> {
    let trimmed = title.trim();
    if trimmed.is_empty() {
        Err("Title must not be empty")
    } else {
        Ok(trimmed)
    }
}

#[cfg(test)]
mod tests {
    use super::validate_title;

    #[test]
    fn trims_surrounding_whitespace() {
        assert_eq!(validate_title("  Rust notes  "), Ok("Rust notes"));
    }

    #[test]
    fn rejects_blank_titles() {
        assert!(validate_title(" \t ").is_err());
    }
}
```

`#[test]` marks a test function. `#[cfg(test)]` includes the module in test builds. `assert_eq!` compares an actual result to an expected one, while `assert!` checks a boolean condition. Unit tests in a child module can access private items in the parent module.

## Integration Tests

Integration tests exercise a library's public API from outside the crate. For a package named `rust-practice`, create `tests/title_validation.rs`:

```rust
use rust_practice::validate_title;

#[test]
fn accepts_a_title_through_the_public_api() {
    assert_eq!(validate_title("Systems notes"), Ok("Systems notes"));
}
```

This example replaces the chapter 5 library. If you kept its binary, update `src/main.rs` to use the new API or keep the catalog module alongside `validate_title`.

## Everyday Checks

Run from the Cargo package directory:

```sh
cargo check
cargo test
cargo fmt --check
cargo clippy --all-targets -- -D warnings
```

`cargo fmt` applies formatting; `cargo fmt --check` reports differences. Clippy suggests improvements, and `-D warnings` makes its warnings fail the command. These tools complement tests. If formatting or Clippy is unavailable, install the corresponding `rustfmt` or `clippy` component through `rustup component add`.

[Next: Closures and Iterators](10-closures-and-iterators.md)

## References

- [Rust Book: Writing Automated Tests](https://doc.rust-lang.org/book/ch11-00-testing.html)
- [Rust Book: Useful Development Tools](https://doc.rust-lang.org/book/appendix-04-useful-development-tools.html)
