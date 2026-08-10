# 04 Code Organization, Packages, and Dependencies

## Table of Contents

1. [Overview](#overview)
2. [Organizing Code](#organizing-code)
   - [Modules, Namespaces, and Files](#modules-namespaces-and-files)
   - [Public and Private APIs](#public-and-private-apis)
   - [Imports and Paths](#imports-and-paths)
3. [Packages and Dependencies](#packages-and-dependencies)
   - [Package Boundaries](#package-boundaries)
   - [Project Layout and Import Direction](#project-layout-and-import-direction)
   - [Declaring Dependencies](#declaring-dependencies)
   - [Reproducible Dependencies](#reproducible-dependencies)
   - [Workspaces and Multi-Package Projects](#workspaces-and-multi-package-projects)
   - [Publishing and Versioning](#publishing-and-versioning)
4. [Concept Mapping](#concept-mapping)
5. [References](#references)

## Overview

As a program grows, code needs both internal structure and clear boundaries for reuse. The usual progression is:

```text
organize related code
→ choose the public API
→ package the code for reuse
→ declare dependencies
→ coordinate multiple related packages
→ release versions for other projects
```

The names differ across languages. Rust has modules, crates, Cargo packages, and workspaces; Go has packages, modules, and workspaces. Python and C++ have comparable ideas but use different tools and conventions.

## Organizing Code

### Modules, Namespaces, and Files

A **module** or **namespace** groups related names and prevents unrelated code from accidentally using the same name. A file often defines part of that organization, but the exact relationship between files and modules is language-specific.

#### Rust

Modules can be nested. `lib.rs` or `main.rs` is the crate root; `mod` adds a child module.

~~~rust
// src/lib.rs
pub mod inventory;

// src/inventory.rs
pub fn count() -> u32 {
    0
}
~~~

The path to `count` is `crate::inventory::count` inside the crate.

#### Go

A Go package is the source files in one directory that declare the same package name. Go has no nested modules inside a package; use another directory and package when a boundary is useful.

~~~go
// inventory/inventory.go
package inventory

func Count() uint {
    return 0
}
~~~

#### Python

A `.py` file is a module. A directory is commonly a package, usually with an `__init__.py` file when an explicit package marker is wanted.

~~~python
# inventory.py
def count() -> int:
    return 0
~~~

#### C++

C++ uses namespaces for name grouping. Header and source files are conventionally paired, but files do not themselves create a namespace.

~~~cpp
// inventory.hpp
namespace inventory {
int count();
}

// inventory.cpp
int inventory::count() {
    return 0;
}
~~~

### Public and Private APIs

A **public API** is the supported surface other code may use. Keeping implementation details private lets you change them without breaking users.

#### Rust

Items are private by default. A caller outside a module can use an item only when every part of its path is visible. `pub` on a module does not automatically make its contents public.

~~~rust
pub mod inventory {
    pub struct Item {
        sku: String, // private field
    }

    impl Item {
        pub fn new(sku: String) -> Self {
            Self { sku }
        }

        pub fn sku(&self) -> &str {
            &self.sku
        }
    }
}
~~~

#### Go

An identifier beginning with an uppercase letter is exported from its package. A lowercase identifier is package-private.

~~~go
package inventory

type Item struct {
    SKU string
}

func NewItem(sku string) Item {
    return Item{SKU: sku}
}

func validateSKU(sku string) bool { // private helper
    return sku != ""
}
~~~

#### Python

Python relies mainly on convention. A leading underscore means “internal”; it does not enforce privacy.

~~~python
class Item:
    def __init__(self, sku: str) -> None:
        self.sku = sku

    def _validate_sku(self) -> bool:
        return bool(self.sku)
~~~

#### C++

Classes use `public`, `private`, and `protected` access sections. Namespaces do not provide a direct privacy boundary; implementation hiding is commonly achieved with headers and source files.

~~~cpp
class Item {
public:
    explicit Item(std::string sku) : sku_(std::move(sku)) {}
    const std::string& sku() const { return sku_; }

private:
    std::string sku_;
};
~~~

### Imports and Paths

Imports make external or distant names convenient to use. They do not change an item's visibility.

#### Rust

~~~rust
use crate::inventory::Item;

let item = Item::new(String::from("A-42"));
~~~

#### Go

~~~go
import "example.com/store/inventory"

item := inventory.NewItem("A-42")
~~~

#### Python

~~~python
from store.inventory import Item

item = Item("A-42")
~~~

#### C++

~~~cpp
#include "inventory.hpp"

inventory::Item item{"A-42"};
~~~

## Packages and Dependencies

### Package Boundaries

A package boundary is a unit you can build, reuse, version, and depend on. It is usually larger than a module or namespace.

#### Rust

A **crate** is a compilation unit: a library crate or binary crate. A Cargo **package** is described by `Cargo.toml` and may contain one library crate and multiple binary crates.

```text
store/                 Cargo package
├── Cargo.toml
└── src/
    ├── lib.rs         library crate
    └── main.rs        binary crate
```

#### Go

A Go **package** is source files in one directory compiled together. A Go **module**, defined by `go.mod`, is one or more packages released and versioned together.

```text
store/                 Go module
├── go.mod
├── inventory/         Go package
└── cmd/store/         package main (executable)
```

#### Python

A distribution package is the unit published to a package index such as PyPI. It can contain multiple import packages and modules.

#### C++

C++ has no single language-level package format. A library target, built with a tool such as CMake, is commonly the reusable unit; a package manager can distribute that library and its metadata.

### Project Layout and Import Direction

Use directories and packages to make dependency direction visible. A small application often has an executable entry point that depends on domain packages, while domain packages do not import the executable.

```text
store/
├── cmd/store/          executable / entry point
├── inventory/          reusable domain package
├── checkout/           reusable domain package
└── tests/              integration tests, where the ecosystem uses them
```

Keep the public API small: callers should import stable domain types and functions, not internal helpers. Avoid circular imports/dependencies; they make initialization and testing harder. Break a cycle by extracting the shared abstraction into a third package, or by inverting the dependency through an interface/trait.

### Declaring Dependencies

Dependency manifests record the code a project needs and, usually, its acceptable versions.

#### Rust

~~~toml
# Cargo.toml
[dependencies]
serde = "1"
inventory = { path = "../inventory" }
~~~

#### Go

~~~go
// go.mod
module example.com/store

go 1.23

require example.com/inventory v1.2.0
~~~

Use `go get example.com/inventory@v1.2.0` to add or update a dependency.

#### Python

~~~toml
# pyproject.toml
[project]
dependencies = [
    "requests>=2.32,<3",
]
~~~

#### C++

With CMake, a project commonly locates an installed dependency and links its target.

~~~cmake
find_package(fmt CONFIG REQUIRED)
target_link_libraries(store PRIVATE fmt::fmt)
~~~

### Reproducible Dependencies

A manifest expresses the dependencies a project is allowed to use; a **lockfile** records the exact dependency versions selected for one build. Cargo uses `Cargo.lock`, Go uses `go.sum`, and Python tools commonly use a tool-specific lockfile. C++ support depends on the selected package manager and build system.

Commit the lockfile for an application so teammates and CI resolve the same dependency graph. Published libraries often commit a lockfile for their own development and tests, but should expose compatible version ranges in their package metadata so downstream applications can resolve a shared graph.

Review direct and transitive dependency updates, security advisories, licenses, and release notes. A dependency declaration is part of the software's supply-chain boundary, not merely build configuration.

### Workspaces and Multi-Package Projects

Large repositories often contain an application plus several related libraries. A workspace coordinates development of those packages without removing their individual boundaries.

#### Rust

A Cargo workspace lists member packages, shares a lockfile and build output directory, and can run commands across members.

~~~toml
# Cargo.toml at the workspace root
[workspace]
resolver = "3"
members = ["app", "inventory"]
~~~

~~~bash
cargo test --workspace
cargo run -p app
~~~

#### Go

A Go workspace's `go.work` file lists local modules that should be used together during development. It is particularly useful when editing a module and one of its dependencies at the same time.

~~~go
// go.work
go 1.23

use (
    ./app
    ./inventory
)
~~~

~~~bash
go work init ./app
go work use ./inventory
~~~

#### Python

Python projects commonly use a monorepo layout with multiple distributions. The exact workspace support depends on the build and dependency tool, such as uv, Poetry, or a build system.

#### C++

CMake can organize multiple library and executable targets in one build with `add_subdirectory`. Other build systems provide comparable project-level coordination.

~~~cmake
add_subdirectory(inventory)
add_subdirectory(app)
~~~

### Publishing and Versioning

Publishing makes a reusable package available outside the local project. Semantic versioning communicates whether a release is compatible with previous users.

#### Rust

Crates are uploaded to a registry, most commonly crates.io. After adding required package metadata and logging in with a crates.io API token, verify the package and publish it.

~~~bash
cargo package --list
cargo publish --dry-run
cargo publish
~~~

Published crates.io versions are permanent: publish a new version instead of overwriting one.

#### Go

Go modules are normally published by pushing a version tag to a public version-control repository. The module path should match the repository location.

~~~bash
go mod tidy
go test ./...
git tag v1.0.0
git push origin v1.0.0
~~~

Do not change the code behind an existing tag; publish a new tag instead.

For every ecosystem, treat a released version as immutable. A breaking public-API change normally requires a major semantic-version increase; compatible features are minor releases and fixes are patch releases.

#### Python

Python distributions are commonly built and uploaded to PyPI. Users install a release with tools such as `pip`.

~~~bash
python -m build
python -m twine upload dist/*
~~~

#### C++

C++ libraries are often released as source archives or Git tags, then made available through a package manager or a project-specific binary registry. The exact workflow depends on the chosen build and package-management tools.

## Concept Mapping

| Purpose | Rust | Go | Python | C++ |
| --- | --- | --- | --- | --- |
| Group names within code | module | package | module/package | namespace |
| Public API | `pub` | capitalized names | convention, often `_name` for internal | `public` members and headers |
| Reusable build unit | library crate | package | import package | library target |
| Versioned release unit | Cargo package/crate | module | distribution | library package, tool-dependent |
| Multi-project development | Cargo workspace | Go workspace | tool-dependent workspace | build-system project |

## References

- [The Rust Book: Packages and Crates](https://doc.rust-lang.org/book/ch07-01-packages-and-crates.html)
- [The Rust Book: Modules and Privacy](https://doc.rust-lang.org/book/ch07-02-defining-modules-to-control-scope-and-privacy.html)
- [The Cargo Book: Workspaces](https://doc.rust-lang.org/cargo/reference/workspaces.html)
- [The Cargo Book: Publishing on crates.io](https://doc.rust-lang.org/cargo/reference/publishing.html)
- [Go Modules Reference](https://go.dev/ref/mod)
- [Go: Publishing a Module](https://go.dev/doc/modules/publishing)
