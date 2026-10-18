# 05 Packages, Crates, and Modules

Use modules to group code and control access. Cargo packages supply the manifest and build targets; crates are the compilation units built from those targets.

## A Small Package Layout

A package can contain a library crate at `src/lib.rs` and a binary crate at `src/main.rs`. Additional binaries can live under `src/bin/`. A module belongs to a crate; putting code in another file does not create another crate.

In the `rust-practice` package from chapter 1, create these files:

`src/lib.rs`:

```rust
pub mod catalog;
```

`src/catalog.rs`:

```rust
pub struct Book {
    title: String,
}

impl Book {
    pub fn new(title: String) -> Self {
        Self { title }
    }

    pub fn title(&self) -> &str {
        &self.title
    }
}
```

`src/main.rs`:

```rust
use rust_practice::catalog::Book;

fn main() {
    let book = Book::new(String::from("Systems notes"));
    println!("{}", book.title());
}
```

The package name `rust-practice` becomes `rust_practice` in a Rust path. If your package has another name, adjust the import.

## Paths and Visibility

`mod catalog;` loads the module; `use` brings a path into the current scope. Within the library, `crate::` starts a path at the library root, and `super::` refers to a parent module. The binary imports the library through its crate name.

`pub` exposes an item through accessible module paths. A public struct still has private fields unless you mark them public individually. Here callers can read the title through a method but cannot assign directly to the field.

## Dependencies

External dependencies are declared under `[dependencies]` in `Cargo.toml`; `cargo add <crate-name>` can add one. `Cargo.lock` records resolved versions for repeatable builds. These introductory examples use only the standard library and need no external dependencies.

[Next: Common Collections](06-common-collections.md)

## References

- [Rust Book: Managing Growing Projects](https://doc.rust-lang.org/book/ch07-00-managing-growing-projects-with-packages-crates-and-modules.html)
