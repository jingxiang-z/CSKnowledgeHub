# 06 Exceptions and Cleanup

Exceptions separate failure handling from the normal return path. Catch a failure where you can respond meaningfully, and use context managers to release resources reliably.

## Raise and Handle Specific Failures

```python
def parse_pages(text):
    try:
        pages = int(text)
    except ValueError as error:
        raise ValueError("Page count must be an integer") from error
    if pages <= 0:
        raise ValueError("Page count must be positive")
    return pages


for text in ["310", "zero", "0"]:
    try:
        pages = parse_pages(text)
    except ValueError as error:
        print(f"Rejected {text!r}: {error}")
    else:
        print(f"Pages: {pages}")
```

`raise ... from error` preserves the original cause. Catch specific exception types and keep the `try` block narrow so unrelated failures are not accidentally handled as expected input errors. Bare `except` also catches process-control exceptions; it is rarely appropriate for application validation.

The `else` block runs when the `try` body completes without an exception. A `finally` block handles cleanup on normal and exceptional exits; avoid returning from it because that can override a result or suppress an exception.

## Context Managers

`with open(path, encoding="utf-8") as file:` closes the file when the block exits, even on an early return or exception. Context managers implement an enter/exit protocol; they also manage locks and other resources. Do not rely on garbage collection timing to close external resources.

Use built-in exceptions such as `ValueError` for an invalid value, or define a subclass of `Exception` when callers need a domain-specific failure type. Assertions check internal assumptions and can be disabled; do not use them as the sole validation of external input.

[Next: Files and the Standard Library](07-files-and-the-standard-library.md)

## References

- [Python tutorial: Errors and exceptions](https://docs.python.org/3/tutorial/errors.html)
- [Python reference: The with statement](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement)
