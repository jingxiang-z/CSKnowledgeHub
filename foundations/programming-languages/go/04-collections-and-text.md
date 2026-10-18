# 04 Collections and Text

Arrays hold a fixed number of elements. Slices describe a region of an underlying array; maps associate keys with values. Strings are immutable byte sequences, conventionally holding UTF-8 text.

## Slice Sharing and Map Lookups

```go
package main

import "fmt"

func main() {
	scores := []int{72, 88, 95}
	view := scores[:2]
	view[0] = 80

	independent := append([]int(nil), scores...)
	independent[0] = 0
	fmt.Println(scores, independent)

	counts := make(map[string]int)
	for _, title := range []string{"Rust", "Go", "Go"} {
		counts[title]++
	}
	count, found := counts["Go"]
	fmt.Println(count, found)
	delete(counts, "Rust")

	text := "Go 世界"
	fmt.Println("bytes:", len(text))
	for offset, character := range text {
		fmt.Printf("byte %d: %c\n", offset, character)
	}
}
```

`[3]int` is an array type and includes its length. `[]int` is a slice type. A slice has a length and capacity; subslicing shares storage. `append` may reuse the underlying array or allocate another one, so always use its returned slice. Do not rely on append to create an independent copy; copy deliberately when needed.

## Zero Values and Iteration

A nil slice has length zero and accepts `append`. A nil map allows reads and deletion but panics on assignment; initialize it with `make` or a map literal before writing. A missing map key returns the element type's zero value; use `value, ok := m[key]` to distinguish absence from a stored zero.

`range` yields an index and element for slices, and a key and value for maps. These values are copies: to change a struct in a slice, assign through its index or use pointers intentionally. Map iteration order is unspecified. Sort keys for stable output. Maps need synchronization when reads overlap writes or when multiple goroutines write.

## Bytes and Runes

`len(text)` counts bytes, and `text[i]` reads one byte. Ranging over a string decodes runes (Unicode code points), with byte offsets as indices. A rune is not always a whole user-perceived character. String slicing uses byte offsets and may split UTF-8 encodings; use text operations that match the intended unit.

[Next: Functions and Interfaces](05-functions-and-interfaces.md)

## References

- [Tour: Slices](https://go.dev/tour/moretypes/7)
- [Tour: Maps](https://go.dev/tour/moretypes/19)
- [Go slices: usage and internals](https://go.dev/blog/slices-intro)
- [Strings, bytes, runes and characters in Go](https://go.dev/blog/strings)
