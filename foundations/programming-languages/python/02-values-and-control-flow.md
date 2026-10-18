# 02 Values and Control Flow

Python names refer to objects, and objects have types. Assignment can bind a name to a different kind of object; operations still require compatible types at runtime.

## Expressions, Branches, and Loops

```python
name = "Ada"
scores = [72, 88, 95]
total = 0
passed = 0

for score in scores:
    total += score
    if score >= 75:
        passed += 1

if scores:
    average = total / len(scores)
    print(f"{name}: {passed} passes, average {average:.1f}")
else:
    print("No scores")

for index in range(3):
    print(index)
```

Indentation defines blocks; use four spaces consistently. A colon introduces the body of a loop, function, or branch. `for` visits items from an iterable, and `range(3)` supplies 0, 1, and 2. Use `while` when repetition depends on a condition, `break` to leave a loop, and `continue` to skip to its next iteration.

## Common Types and Operators

Integers have arbitrary precision subject to memory limits. `float` typically uses binary floating-point, so many decimal fractions are approximate. `/` performs true division; `//` performs floor division. Strings are immutable Unicode text, and `len(text)` counts code points rather than encoded bytes or necessarily user-perceived characters.

`None` represents absence. Test it with `value is None`. Use `==` for value equality and `is` for object identity. Empty containers, zero, `False`, and `None` are false in a condition. `and` and `or` short-circuit and return one of their operands, which need not be a boolean.

`int("42")` parses an integer, but `int("forty")` raises an exception. Python does not automatically combine a string and integer with `+`; use explicit conversion or an f-string. Comments start with `#`.

[Next: Collections, References, and Copying](03-collections-references-and-copying.md)

## References

- [Python tutorial: An informal introduction](https://docs.python.org/3/tutorial/introduction.html)
- [Python tutorial: More control flow tools](https://docs.python.org/3/tutorial/controlflow.html)
