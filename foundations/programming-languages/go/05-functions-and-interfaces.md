# 05 Functions and Interfaces

Functions are values and can capture surrounding variables. Interfaces describe behavior through method sets, allowing callers to depend on a small contract.

## Pass Behavior and Values

```go
package main

import "fmt"

type Labeler interface {
	Label() string
}

type Book struct {
	Title string
}

func (b Book) Label() string {
	return b.Title
}

func printLabel(item Labeler, decorate func(string) string) {
	fmt.Println(decorate(item.Label()))
}

func main() {
	prefix := "Available: "
	decorate := func(text string) string {
		return prefix + text
	}
	book := Book{Title: "Systems notes"}
	printLabel(book, decorate)
	prefix = "Returned: "
	printLabel(book, decorate)
}
```

The closure captures `prefix`, so its second call sees the updated value. Captured variables may outlive the function call that created the closure. Sharing them between goroutines still requires synchronization.

## Implicit Interface Implementation

`Book` implements `Labeler` by having a matching method; no declaration of intent is needed. Define small interfaces around the operations a caller needs. Standard interfaces such as `io.Reader` let unrelated types work with the same functions.

With the value receiver above, both `Book` and `*Book` implement `Labeler`. If `Label` instead had a pointer receiver, only `*Book` would implement the interface. Automatic address-taking in a direct method call does not change interface satisfaction.

## Interface Values and Nil

An interface value carries a dynamic concrete type and value. It equals `nil` only when both are absent. An interface containing a typed nil pointer is non-nil, which matters especially when returning errors.

Use `value, ok := item.(ConcreteType)` for a checked type assertion, or a type switch when you need different handling by dynamic type. A single-result assertion panics if it fails. `any` is an alias for the empty interface; use it when arbitrary values are actually required, preserving concrete types elsewhere.

[Next: Errors and Deferred Cleanup](06-errors-and-deferred-cleanup.md)

## References

- [Tour: Function values and closures](https://go.dev/tour/moretypes/24)
- [Tour: Interfaces](https://go.dev/tour/methods/9)
- [Go FAQ: Why is my nil error value not equal to nil?](https://go.dev/doc/faq#nil_error)
