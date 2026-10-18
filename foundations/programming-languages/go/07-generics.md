# 07 Generics

Generics express operations shared by multiple concrete types. A constraint specifies which types may be used and which operations are valid in the generic code.

## Preserve Element Types

```go
package main

import "fmt"

func unique[T comparable](values []T) []T {
	seen := make(map[T]bool)
	var result []T
	for _, value := range values {
		if !seen[value] {
			seen[value] = true
			result = append(result, value)
		}
	}
	return result
}

type PageCount int

type PageNumber interface {
	~int | ~int64
}

func double[T PageNumber](value T) T {
	return value + value
}

func main() {
	fmt.Println(unique([]string{"Go", "Rust", "Go"}))
	fmt.Println(unique([]int{3, 3, 8}))
	fmt.Println(double(PageCount(12)))
}
```

`T` is a type parameter. `comparable` permits the equality operations needed for a map key. The compiler infers `T` from the slice passed to `unique`; `unique[string](...)` is an explicit alternative. Unlike `[]any`, `[]T` preserves one concrete element type throughout a call.

## Constraints and Type Sets

`~int` includes types whose underlying type is `int`, such as `PageCount`. `|` forms a union, so `PageNumber` permits types based on `int` or `int64`. Such an interface is a constraint, not a type for ordinary runtime values.

Only operations valid for every type allowed by a constraint are available in the function body. `any` places no restriction on type arguments but does not grant arithmetic or comparison operations. Generic types are also possible, for example a container whose fields use a type parameter.

## Choose an Abstraction

Use an ordinary function when one concrete type is sufficient. Use a small interface when callers need common behavior, such as reading bytes. Use type parameters when the same algorithm or container should preserve different concrete types. Avoid introducing a generic abstraction before there is useful shared logic.

[Next: Goroutines and Channels](08-goroutines-and-channels.md)

## References

- [Tour: Generics](https://go.dev/tour/generics/1)
- [Go tutorial: Getting started with generics](https://go.dev/doc/tutorial/generics)
- [Go specification: Interface types](https://go.dev/ref/spec#Interface_types)
