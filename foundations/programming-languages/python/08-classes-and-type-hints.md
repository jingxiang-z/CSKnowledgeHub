# 08 Classes and Type Hints

Classes combine state with behavior. Type hints document expected values and support static analysis, while runtime validation remains explicit.

## Define a Model and a Behavioral Contract

```python
from dataclasses import dataclass
from typing import Protocol


class Labeler(Protocol):
    def label(self) -> str: ...


@dataclass
class Book:
    title: str
    checked_out: bool = False

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("Title must not be blank")

    def label(self) -> str:
        return self.title

    def check_out(self) -> None:
        if self.checked_out:
            raise ValueError("Book is already checked out")
        self.checked_out = True


def print_label(item: Labeler) -> None:
    print(item.label())


book = Book("Systems notes")
book.check_out()
print_label(book)
```

`self` is the instance passed to a method. `@dataclass` generates operations such as initialization and representation from declared fields; `__post_init__` runs after generated initialization. It does not enforce field types or automatically validate later assignments.

## State and Encapsulation

Instance attributes hold per-object state. A mutable class attribute is shared across instances; initialize per-object lists in `__init__` or use `dataclasses.field(default_factory=list)`. A leading underscore communicates internal use, but Python does not enforce private fields like C++. A property can mediate access when validation is needed.

Use composition to combine models. Inheritance can specialize behavior, but a function can also accept any object with the required methods, often called duck typing.

## Static Contracts

`Protocol` describes structural compatibility for type checkers: `Book` need not inherit from `Labeler`. Annotations such as `list[Book]` and `Book | None` express collections and optional values. Python does not normally enforce these annotations at runtime; use an optional type checker separately when useful.

[Next: Iterators and Generators](09-iterators-and-generators.md)

## References

- [Python tutorial: Classes](https://docs.python.org/3/tutorial/classes.html)
- [Standard library: dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [Standard library: typing](https://docs.python.org/3/library/typing.html)
