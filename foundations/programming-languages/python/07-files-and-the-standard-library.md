# 07 Files and the Standard Library

Use standard library modules for paths, serialization, command-line arguments, and temporary files. Separate file access from the logic that interprets the content.

## Read and Write Structured Text

```python
import json
from pathlib import Path
from tempfile import TemporaryDirectory


with TemporaryDirectory() as directory:
    path = Path(directory) / "catalog.json"
    books = [{"title": "Systems notes", "pages": 310}]
    with path.open("w", encoding="utf-8") as file:
        json.dump(books, file, ensure_ascii=False, indent=2)

    with path.open(encoding="utf-8") as file:
        loaded = json.load(file)
    for book in loaded:
        print(f"{book['title']}: {book['pages']} pages")
```

`Path` composes paths without manually joining separator characters. Relative paths are resolved against the process's current working directory, not automatically against the script directory. The temporary directory context cleans up this example's files.

## Text, Bytes, and Validation

Text files decode bytes into `str`; binary mode works with `bytes`. Specify an encoding when a format requires it. Reading with `for line in file` can process a file incrementally instead of loading all its contents into memory.

JSON decoding produces ordinary lists, dictionaries, strings, numbers, booleans, and `None`. Successful parsing does not establish that the result has the expected application schema. Validate required fields and value constraints separately. A missing file raises `FileNotFoundError`; malformed JSON raises `json.JSONDecodeError`.

For a command-line tool, `argparse` handles options, help text, and simple conversions. Use `logging` for operational messages, `collections` for specialized containers, and `datetime` for date/time values. Prefer looking up a focused standard library API before adding a dependency.

[Next: Classes and Type Hints](08-classes-and-type-hints.md)

## References

- [Python tutorial: Input and output](https://docs.python.org/3/tutorial/inputoutput.html)
- [Standard library: pathlib](https://docs.python.org/3/library/pathlib.html)
- [Standard library: json](https://docs.python.org/3/library/json.html)
- [Standard library: argparse](https://docs.python.org/3/library/argparse.html)
