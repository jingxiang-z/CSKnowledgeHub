# 05 Modules and Packages

A module is an importable unit, commonly a `.py` file. A package groups modules under an import path. Keep reusable operations separate from program entry points.

## A Small Package Layout

Create a `catalog` directory containing an empty `__init__.py` and these files.

`catalog/labels.py`:

```python
def label(title):
    return f"Book: {title}"
```

`catalog/__main__.py`:

```python
from .labels import label


def main():
    print(label("Systems notes"))


if __name__ == "__main__":
    main()
```

Run `python3 -m catalog` from the parent directory. The `-m` option executes the package's `__main__` module. A regular package uses `__init__.py`; namespace packages are a separate mechanism that can omit it.

## Imports and Boundaries

`import catalog.labels` binds the module path; `from catalog.labels import label` binds the function name locally. The relative import `.labels` refers to a sibling inside the same package. Run this entry point with `-m` rather than executing `catalog/__main__.py` by file path, which loses the intended package context.

Importing a module executes its top-level statements on the first ordinary import in a process and then normally reuses the cached module. Keep unexpected file writes, network calls, and application startup out of import-time code.

A leading underscore marks an internal name by convention; it does not prevent access. Avoid wildcard imports because they obscure where names came from. Names such as `json.py` can accidentally shadow standard library modules if placed on the import search path.

An import package name and a distribution name installed by pip need not be identical. Project metadata and distribution publishing are separate topics from this small source layout.

[Next: Exceptions and Cleanup](06-exceptions-and-cleanup.md)

## References

- [Python tutorial: Modules](https://docs.python.org/3/tutorial/modules.html)
- [Python reference: The import system](https://docs.python.org/3/reference/import.html)
