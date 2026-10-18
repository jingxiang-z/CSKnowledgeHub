# 01 Getting Started and Common Concepts

Cargo manages Rust projects, dependencies, builds, and tests. Start with a small binary crate and learn the syntax needed to follow the later examples.

## Create and Run a Program

Install the stable toolchain using the [official installation instructions](https://www.rust-lang.org/tools/install). Then create a practice project outside this documentation directory:

```sh
rustc --version
cargo --version
cargo new rust-practice --edition 2024
cd rust-practice
cargo run
cargo check
```

`Cargo.toml` contains package metadata and dependencies; `src/main.rs` contains the binary entry point. `cargo check` checks the code without building an executable. Replace `src/main.rs` with a chapter's standalone example to try it.

## Values, Functions, and Control Flow

```rust
fn passes(score: u32) -> bool {
    score >= 75
}

fn main() {
    let name: &str = "Ada";
    let scores: [u32; 3] = [72, 88, 95];
    let mut passed = 0;

    for score in scores {
        if passes(score) {
            passed += 1;
        }
    }

    let label = if passed > 0 { "has passes" } else { "no passes" };
    println!("{name}: {passed} passes ({label})");
}
```

Bindings are immutable unless declared with `mut`. A new `let` can shadow an earlier binding, even with a different type. Integers such as `u32`, booleans, and tuples are common value types. Arrays have a fixed length; vectors arrive in chapter 6.

Function parameters need types. The final expression without a semicolon supplies the return value; adding a semicolon turns it into a statement. Both branches of an `if` expression must produce compatible types. Use `for` for traversal, `while` for a condition, and `loop` with `break` for an open-ended loop.

`println!` is a macro, indicated by `!`. Normal functions such as `passes` have no exclamation mark. Line comments start with `//`.

[Next: Ownership, References, and Slices](02-ownership-references-and-slices.md)

## References

- [Rust Book: Getting Started](https://doc.rust-lang.org/book/ch01-00-getting-started.html)
- [Rust Book: Common Programming Concepts](https://doc.rust-lang.org/book/ch03-00-common-programming-concepts.html)
