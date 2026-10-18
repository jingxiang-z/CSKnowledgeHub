# 10 Tests and Tooling

Tests check behavior that type checking cannot establish. Use the standard `testing` package to cover expected results, boundary cases, and failure paths.

## Write a Table Test

In a separate practice module, create `title.go`:

```go
package catalog

import (
	"errors"
	"strings"
)

func ValidateTitle(title string) (string, error) {
	trimmed := strings.TrimSpace(title)
	if trimmed == "" {
		return "", errors.New("title must not be empty")
	}
	return trimmed, nil
}
```

Then add `title_test.go` in the same directory:

```go
package catalog

import "testing"

func TestValidateTitle(t *testing.T) {
	tests := []struct {
		name    string
		input   string
		want    string
		wantErr bool
	}{
		{name: "trims", input: "  Go notes  ", want: "Go notes"},
		{name: "blank", input: " \t ", wantErr: true},
		{name: "unicode", input: " 世界 ", want: "世界"},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := ValidateTitle(tt.input)
			if (err != nil) != tt.wantErr {
				t.Fatalf("error = %v, wantErr %v", err, tt.wantErr)
			}
			if got != tt.want {
				t.Errorf("title = %q, want %q", got, tt.want)
			}
		})
	}
}
```

Test files end in `_test.go`; test functions take `*testing.T` and use a `Test` prefix. `Fatalf` stops the current test, while `Errorf` records a failure and continues. A test in package `catalog` can access unexported declarations; package `catalog_test` tests only the public API through an import.

## Everyday Checks

From the module root:

```sh
go fmt ./...
go vet ./...
go test ./...
go test -race ./...
go test -cover ./...
```

Formatting applies Go's standard layout. Vet detects suspicious code. The race detector catches data races on executed paths; a clean run does not prove untested paths safe. It requires a supported platform and a suitable C toolchain. Coverage reports which statements ran, not whether assertions are useful.

Return to the [Go learning path](README.md).

## References

- [Go tutorial: Add a test](https://go.dev/doc/tutorial/add-a-test)
- [Standard library: testing](https://pkg.go.dev/testing)
- [Go command documentation](https://pkg.go.dev/cmd/go)
- [Data race detector](https://go.dev/doc/articles/race_detector)
