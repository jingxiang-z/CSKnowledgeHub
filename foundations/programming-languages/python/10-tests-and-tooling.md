# 10 Tests and Tooling

Use tests to check expected behavior and failure paths. Python's standard library provides unit testing, debugging, logging, and profiling without additional packages.

## Test a Public Operation

`titles.py`:

```python
def validate_title(title: str) -> str:
    trimmed = title.strip()
    if not trimmed:
        raise ValueError("Title must not be blank")
    return trimmed
```

`test_titles.py`, in the same directory:

```python
import unittest

from titles import validate_title


class TitleTests(unittest.TestCase):
    def test_trims_titles(self):
        for raw, expected in [(" Go notes ", "Go notes"), (" 世界 ", "世界")]:
            with self.subTest(raw=raw):
                self.assertEqual(validate_title(raw), expected)

    def test_rejects_blank_titles(self):
        for raw in ["", " \t "]:
            with self.subTest(raw=raw):
                with self.assertRaises(ValueError):
                    validate_title(raw)


if __name__ == "__main__":
    unittest.main()
```

Run `python3 -m unittest discover -v` from that directory. Discovery finds files matching `test*.py`; methods beginning with `test` are test cases. Subtests identify individual input failures. Assertions provided by `unittest` remain active even when ordinary Python `assert` statements are optimized away.

## Everyday Tools

Use `python3 -m pdb main.py` to debug a script or call `breakpoint()` at a point of interest. `python3 -m cProfile main.py` measures where execution time is spent. Read tracebacks from the exception message back through the relevant call frames.

[PEP 8](https://peps.python.org/pep-0008/) describes common formatting and naming conventions. Formatters, linters, and type checkers are optional external tools; use the project's chosen configuration when available. Syntax checks and passing type checks do not replace behavioral tests.

Return to the [Python learning path](README.md).

## References

- [Standard library: unittest](https://docs.python.org/3/library/unittest.html)
- [Standard library: pdb](https://docs.python.org/3/library/pdb.html)
- [Standard library: Python profilers](https://docs.python.org/3/library/profile.html)
- [PEP 8: Style Guide for Python Code](https://peps.python.org/pep-0008/)
