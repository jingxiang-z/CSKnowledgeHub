# 02 Ownership, References, and Slices

Ownership determines who is responsible for a value. Borrowing lets code use a value without taking ownership, while the compiler checks that references remain valid.

## Moves and Copies

Assigning an owned `String` to another binding moves it: the old binding can no longer be used. Types that implement `Copy`, such as `u32`, can be copied implicitly. Use `clone()` when you intentionally need an independent copy of a string.

```rust
fn main() {
    let original = String::from("Rust notes");
    let moved = original;
    // original is no longer usable.
    let independent = moved.clone();
    println!("{moved} / {independent}");
}
```

Passing a value to a function follows the same ownership rules as assignment. Returning a value can transfer ownership back to the caller. When an owned value goes out of scope, its cleanup runs.

## Borrow Instead of Moving

```rust
fn first_word(text: &str) -> &str {
    text.split_whitespace().next().unwrap_or("")
}

fn add_suffix(text: &mut String) {
    text.push_str(" updated");
}

fn main() {
    let mut title = String::from("Rust notes");
    let word = first_word(&title);
    println!("{word}");
    // The shared borrow is no longer used, so mutation is allowed.
    add_suffix(&mut title);
    println!("{title}");
}
```

`&T` borrows shared access; `&mut T` borrows exclusive access. While conflicting accesses overlap, you can have shared borrows or one exclusive borrow. A borrow often ends at its last use, before the end of the enclosing block. Ordinary references cannot outlive their referent.

## Slices

`String` owns growable UTF-8 text; `&str` borrows a string slice. Prefer `&str` for a parameter that only reads text because callers can supply either a string literal or a borrowed `String`. Similarly, `&[T]` borrows a sequence of elements from an array or vector.

String slice boundaries must be UTF-8 character boundaries. Do not assume a byte offset is a character position. `first_word` above avoids manual indexing. Its `unwrap_or("")` supplies a default for an empty input without panicking.

[Next: Structs and Methods](03-structs-and-methods.md)

## References

- [Rust Book: Understanding Ownership](https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html)
