# 02 Values, Functions, and Control Flow

Go uses static types, explicit control flow, and functions that can return multiple results. Uninitialized variables receive a zero value appropriate to their type.

## Declare Values and Call Functions

```go
package main

import "fmt"

const passMark = 75

func summarize(scores []int) (int, int) {
	total, passed := 0, 0
	for _, score := range scores {
		total += score
		if score >= passMark {
			passed++
		}
	}
	return total, passed
}

func main() {
	var name string // Zero value: "".
	name = "Ada"
	scores := []int{72, 88, 95}
	total, passed := summarize(scores)
	switch passed {
	case 0:
		fmt.Println("No passes")
	default:
		fmt.Printf("%s: %d passes, total %d\n", name, passed, total)
	}
}
```

`var` can appear at package or function scope. `:=` declares variables inside a function and infers their types; it must introduce at least one new non-blank variable in the same scope. `const` defines a compile-time constant. Common types include `bool`, `int`, `uint64`, `float64`, and `string`. Numeric conversions are explicit, for example `float64(total)`.

Function parameter types follow their names. Multiple return values are separate results, not a tuple object. `[]int` is a slice of integers, covered in chapter 4. In the loop, `_` discards the index and `score` receives each element.

## Branch and Loop

Go has one loop keyword, `for`: use a three-part loop, a condition-only loop, an endless `for`, or `for ... range`. `if` conditions need no parentheses; braces are required. Keep the opening brace on the same line as the condition.

An `if` can include a short initialization statement whose bindings are scoped to its branches. A `switch` selects a case and does not fall through by default. `break` leaves a loop or switch; `continue` advances a loop.

[Next: Pointers, Structs, and Methods](03-pointers-structs-and-methods.md)

## References

- [Tour: Packages, variables, and functions](https://go.dev/tour/basics/1)
- [Tour: Flow control](https://go.dev/tour/flowcontrol/1)
