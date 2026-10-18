# 10 Closures and Iterators

Closures are anonymous functions that can capture surrounding values. Iterators describe traversal and let you combine filtering, transformation, and aggregation.

## Transform a Borrowed Collection

```rust
fn main() {
    let threshold = 75;
    let scores = vec![62, 75, 91, 44];

    let passing: Vec<i32> = scores
        .iter()
        .copied()
        .filter(|score| *score >= threshold)
        .collect();

    let total: i32 = passing.iter().sum();
    let labels: Vec<String> = passing
        .iter()
        .map(|score| format!("PASS: {score}"))
        .collect();

    println!("{labels:?}, total={total}");
    println!("Original scores: {scores:?}");
}
```

The closure `|score| *score >= threshold` captures `threshold` from the surrounding scope. `iter()` borrows elements, and `copied()` copies the integers into the iterator pipeline. `filter` still receives a reference to each candidate item, so the predicate dereferences `score`.

## Adapters and Consumers

`map` and `filter` are lazy adapters: creating them does not traverse the collection. A consumer such as `collect`, `sum`, or `count`, or a `for` loop, drives iteration. The `Vec<i32>` annotation tells `collect` which collection to build.

| Method on a vector | Access to elements |
|---|---|
| `iter()` | Borrowed `&T` |
| `iter_mut()` | Borrowed `&mut T` |
| `into_iter()` | Owned `T`; consumes the vector |

Choose based on whether you need to read, mutate, or take ownership. An iterator is stateful: calling `next()` advances it. A consuming operation takes that iterator, though the source collection can remain available when it was only borrowed.

## Closure Captures

The compiler infers whether a closure borrows, mutably borrows, or takes ownership of captured values based on its body. `move` forces captures by value; a non-`Copy` value is moved into the closure. The traits `Fn`, `FnMut`, and `FnOnce` describe how a closure can be called. You do not need to write those bounds for the pipelines above.

Return to the [Rust learning path](README.md).

## References

- [Rust Book: Iterators and Closures](https://doc.rust-lang.org/book/ch13-00-functional-features.html)
