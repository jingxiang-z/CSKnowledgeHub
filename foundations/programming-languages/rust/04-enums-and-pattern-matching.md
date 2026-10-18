# 04 Enums and Pattern Matching

An enum describes a value that can be one of several variants. Each variant can carry its own data, making states explicit in the type system.

## Match on a State

```rust
enum CheckoutState {
    Available,
    Borrowed { reader: String },
}

fn describe(state: &CheckoutState) -> String {
    match state {
        CheckoutState::Available => String::from("On shelf"),
        CheckoutState::Borrowed { reader } => format!("With {reader}"),
    }
}

fn main() {
    let states = [
        CheckoutState::Available,
        CheckoutState::Borrowed { reader: String::from("Ada") },
    ];
    for state in &states {
        println!("{}", describe(state));
    }

    let title: Option<&str> = Some("Systems notes");
    if let Some(text) = title {
        println!("Found {text}");
    }
}
```

A `match` must cover every possible input. This means adding an enum variant prompts you to handle it in existing matches. A wildcard `_` handles remaining cases when their individual values do not matter. Matching through a reference lets you inspect data without moving it out.

## Represent Absence with Option

`Option<T>` has two variants: `Some(T)` and `None`. A lookup can return `Option<&Book>` to express that a book may be missing. Handle absence with `match`, `if let`, or a default such as `unwrap_or`.

`if let` is convenient when only one pattern needs action. Use `let Some(value) = expression else { return; };` when a failed match should leave the current path early; the `else` block must diverge, for example with `return` or `panic!`.

Avoid using `unwrap()` on an optional value unless absence should terminate execution with a panic. Missing data is often an ordinary outcome.

[Next: Packages, Crates, and Modules](05-packages-crates-and-modules.md)

## References

- [Rust Book: Enums and Pattern Matching](https://doc.rust-lang.org/book/ch06-00-enums.html)
