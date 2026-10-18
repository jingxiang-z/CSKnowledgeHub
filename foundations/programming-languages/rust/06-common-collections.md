# 06 Common Collections

Use `Vec<T>` for a growable sequence, `String` for owned UTF-8 text, and `HashMap<K, V>` for key-based lookup. All three own their stored data.

## Store and Look Up Values

```rust
use std::collections::HashMap;

fn main() {
    let mut titles: Vec<String> = vec![String::from("Systems notes")];
    titles.push(String::from("Rust notes"));

    if let Some(first) = titles.get(0) {
        println!("First: {first}");
    }

    let mut counts: HashMap<String, usize> = HashMap::new();
    for title in &titles {
        let category = title.split_whitespace().next().unwrap_or("Other");
        *counts.entry(category.to_string()).or_insert(0) += 1;
    }

    if let Some(count) = counts.get("Rust") {
        println!("Rust titles: {count}");
    }
    println!("Titles still available: {}", titles.len());
}
```

`get` returns an `Option` instead of panicking when an index or key is missing. Vector indexing with `titles[index]` panics if the index is out of bounds. Inserting an existing map key replaces its value; `entry` lets you update a value or initialize it when missing.

## Ownership During Traversal

| Expression | Items produced for a vector |
|---|---|
| `for value in &values` | Shared references |
| `for value in &mut values` | Mutable references |
| `for value in values` | Owned elements; consumes the vector |

In the example, borrowing `titles` lets it remain usable after the loop. The map owns new `String` keys produced by `to_string()`. The `*` dereferences the mutable reference returned by `or_insert`, allowing the count to change.

## Text Is UTF-8

`String::len()` counts bytes. Use `.chars()` to traverse Unicode scalar values or `.split_whitespace()` for whitespace-separated fields. Scalar values are not always whole user-perceived characters. Strings do not support integer indexing, and slicing at an invalid byte boundary panics.

`HashMap` iteration order is unspecified. Sort extracted entries or use an ordered collection when output order matters, as the library catalog does for available books.

[Next: Error Handling](07-error-handling.md)

## References

- [Rust Book: Common Collections](https://doc.rust-lang.org/book/ch08-00-common-collections.html)
