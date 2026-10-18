# 06 Errors and Deferred Cleanup

Go reports expected failures with explicit error return values. Handle an error where you can recover, or return it with enough context for the caller.

## Return, Wrap, and Inspect Errors

```go
package main

import (
	"errors"
	"fmt"
	"strconv"
)

var ErrInvalidPages = errors.New("page count must be positive")

func parsePages(input string) (int, error) {
	pages, err := strconv.Atoi(input)
	if err != nil {
		return 0, fmt.Errorf("parse pages %q: %w", input, err)
	}
	if pages <= 0 {
		return 0, ErrInvalidPages
	}
	return pages, nil
}

func main() {
	defer fmt.Println("Finished validation")
	for _, input := range []string{"310", "zero", "0"} {
		pages, err := parsePages(input)
		if errors.Is(err, ErrInvalidPages) {
			fmt.Println("Choose a positive count")
			continue
		}
		if err != nil {
			fmt.Println(err)
			continue
		}
		fmt.Println("Pages:", pages)
	}
}
```

`error` is an interface with an `Error() string` method. A nil error means success. Check the error before relying on other results. `%w` wraps an underlying error; `errors.Is` checks identity through wrapping, while `errors.As` finds a matching error type. Avoid identifying errors by comparing message strings.

## Defer Cleanup After Acquisition

`defer` schedules a call for when the surrounding function returns, including ordinary early returns. Deferred calls run in reverse order; their arguments are evaluated when the `defer` statement executes.

For a file, first check that `os.Open` succeeded, then defer `file.Close()`. A defer inside a loop waits for the whole function to finish, not that iteration; use a helper function when each iteration should release its resource promptly. If a close or flush error matters, propagate it deliberately rather than silently discarding it.

Garbage collection does not replace this resource management. `panic` is for exceptional failures and violated assumptions; `recover` is a specialized boundary mechanism. Keep normal validation on the error-return path.

[Next: Generics](07-generics.md)

## References

- [Tour: Errors](https://go.dev/tour/methods/19)
- [Tour: Defer](https://go.dev/tour/flowcontrol/12)
- [Standard library: errors](https://pkg.go.dev/errors)
- [Go blog: Defer, Panic, and Recover](https://go.dev/blog/defer-panic-and-recover)
