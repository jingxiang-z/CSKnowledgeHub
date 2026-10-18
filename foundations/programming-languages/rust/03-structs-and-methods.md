# 03 Structs and Methods

A struct groups related fields into one type. Methods keep operations next to the data they inspect or change.

## Define a Type and Its Behavior

```rust
#[derive(Debug)]
struct Book {
    title: String,
    checked_out: bool,
}

impl Book {
    fn new(title: String) -> Self {
        Self { title, checked_out: false }
    }

    fn title(&self) -> &str {
        &self.title
    }

    fn check_out(&mut self) {
        self.checked_out = true;
    }
}

fn main() {
    let mut book = Book::new(String::from("Systems notes"));
    println!("{}", book.title());
    book.check_out();
    println!("{book:?}");
}
```

`Self` names the type being implemented. `new` is an associated function called with `Book::new`; it is a convention, not a special constructor keyword. Field shorthand lets `title` stand for `title: title`.

## Choose the Receiver

| Receiver | Use |
|---|---|
| `&self` | Read the existing value |
| `&mut self` | Change the existing value |
| `self` | Consume the value, unless its type is `Copy` |

The returned `&str` borrows the book's title rather than copying it. The `Debug` derive generates support for diagnostic formatting with `{:?}`.

Fields are private outside their defining module by default, but code in that module can still access them. Put a type in its own module and expose selected `pub` methods when callers should not directly change its fields. Chapter 5 covers that boundary.

The example allows repeated checkout and empty titles for simplicity. The existing library catalog uses `Result` to enforce those rules; chapter 7 explains that return type.

[Next: Enums and Pattern Matching](04-enums-and-pattern-matching.md)

## References

- [Rust Book: Using Structs to Structure Related Data](https://doc.rust-lang.org/book/ch05-00-structs.html)
