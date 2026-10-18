# 01 Getting Started, Packages, and Modules

A Go module groups packages under a module path and records dependencies in `go.mod`. A package groups source files in a directory; an executable uses package `main` and a `main` function.

## Create a Practice Module

Install Go using the [official instructions](https://go.dev/doc/install). Outside this documentation directory, run:

```sh
go version
mkdir go-practice
cd go-practice
go mod init example.com/go-practice
```

Create a `catalog` directory and add these two files.

`catalog/book.go`:

```go
package catalog

type Book struct {
	title string
}

func NewBook(title string) Book {
	return Book{title: title}
}

func (b Book) Title() string {
	return b.title
}
```

`main.go`:

```go
package main

import (
	"fmt"

	"example.com/go-practice/catalog"
)

func main() {
	book := catalog.NewBook("Systems notes")
	fmt.Println(book.Title())
}
```

From the module root, run `go run .` to execute or `go build ./...` to compile all packages. Later chapters explain the struct and method syntax used here.

## Imports and Visibility

An import path combines the module path with the package's directory. The `catalog` package above is local to this module and requires no download. Standard library packages such as `fmt` are included with Go.

An identifier beginning with an uppercase letter is exported from its package. `Book`, `NewBook`, and `Title` are exported; the `title` field is accessible only within `catalog`. Files in the same package can access each other's unexported declarations. Go rejects unused imports and unused local variables.

## Dependencies

For external packages, `go get <module-path>@<version>` adds or updates a dependency. `go mod tidy` reconciles dependencies with imports. `go.sum` records dependency checksums; it is not a lockfile. These chapters use only the standard library.

Use a module path you control when publishing code. `example.com/go-practice` is only a local teaching placeholder. A module's `go` directive states its minimum Go version; start with a current stable installation.

[Next: Values, Functions, and Control Flow](02-values-functions-and-control-flow.md)

## References

- [Go tutorial: Getting started](https://go.dev/doc/tutorial/getting-started)
- [Organizing a Go module](https://go.dev/doc/modules/layout)
- [Managing dependencies](https://go.dev/doc/modules/managing-dependencies)
