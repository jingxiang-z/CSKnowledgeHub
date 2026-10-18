# 08 Generics, Traits, and Lifetimes

Generics let code work with multiple types. Trait bounds state which operations those types support. Lifetime annotations describe how borrowed inputs and outputs relate.

## Generic Data and Shared Behavior

```rust
struct Entry<T> {
    value: T,
}

trait Label {
    fn label(&self) -> &str;
}

impl Label for Entry<String> {
    fn label(&self) -> &str {
        &self.value
    }
}

fn print_label<T: Label>(item: &T) {
    println!("{}", item.label());
}

fn choose_label<'a>(first: &'a str, second: &'a str) -> &'a str {
    if first.len() >= second.len() { first } else { second }
}

fn main() {
    let entry = Entry { value: String::from("Rust notes") };
    print_label(&entry);
    let other = String::from("Systems notes");
    println!("{}", choose_label(entry.label(), &other));
}
```

`Entry<T>` can store different types, but this `Label` implementation applies specifically to `Entry<String>`. `print_label` accepts any concrete type implementing `Label`. Trait bounds can also appear in a `where` clause when a signature becomes crowded.

Generic calls normally use static dispatch. A borrowed `&dyn Label` can support runtime dispatch when you need to handle different implementing types through a common interface. Start with generics until that requirement appears.

## Borrow Relationships

In `choose_label`, `'a` relates both inputs to the output. The returned reference can only be used for a lifetime supported by both input borrows. The annotation does not keep either string alive or change when it is dropped.

Rust often infers these relationships. For example, a function with one borrowed input can usually return a reference tied to that input without annotations. A method returning a borrow is commonly tied to `&self`, as in `label` above. Multiple borrowed inputs may require an explicit relationship.

If a function creates a new string locally, return an owned `String`; returning a reference to that local value would leave a dangling reference. Lifetime annotations cannot repair that design.

[Next: Tests and Tooling](09-tests-and-tooling.md)

## References

- [Rust Book: Generic Types, Traits, and Lifetimes](https://doc.rust-lang.org/book/ch10-00-generics.html)
