# 03 Pointers, Structs, and Methods

Structs group related fields. Assignment and function calls copy values; pointers let multiple parts of a program access the same value.

## Read and Change a Struct

```go
package main

import "fmt"

type Book struct {
	title      string
	checkedOut bool
}

func (b Book) Title() string {
	return b.title
}

func (b *Book) CheckOut() {
	b.checkedOut = true
}

func main() {
	book := Book{title: "Systems notes"}
	copied := book
	shared := &book
	shared.CheckOut()
	fmt.Println(book.Title(), book.checkedOut, copied.checkedOut)
}
```

`&book` produces a pointer; `*Book` is a pointer type. `*pointer` dereferences a pointer, though Go automatically handles dereferencing for struct field access. Calling a pointer-receiver method on an addressable value such as `book.CheckOut()` also works.

A value receiver such as `(b Book)` operates on a copy. A pointer receiver such as `(b *Book)` can change the original struct and avoids copying a large value. Prefer consistent receiver choices for a type. A nil pointer refers to no value; dereferencing it panics.

## Copies Can Still Share Data

In this example, changing `book.checkedOut` leaves `copied.checkedOut` unchanged. However, copying a struct containing slices, maps, or pointers does not deeply copy their referenced data. Chapter 4 shows slice sharing.

Go's garbage collector keeps reachable ordinary Go data alive, including values returned by pointer from functions. This does not close files or coordinate concurrent access: cleanup and synchronization remain explicit responsibilities.

## Composition and Boundaries

Put one named type inside another to compose behavior. Embedding can promote fields and methods, but does not create class inheritance. Unexported fields limit access from other packages, as in chapter 1; code within the defining package can still modify them.

[Next: Collections and Text](04-collections-and-text.md)

## References

- [Tour: Pointers and structs](https://go.dev/tour/moretypes/1)
- [Tour: Methods](https://go.dev/tour/methods/1)
- [Effective Go: Embedding](https://go.dev/doc/effective_go#embedding)
