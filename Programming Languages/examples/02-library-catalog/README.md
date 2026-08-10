# Library Catalog

Model a small library that tracks books and whether they are checked out.

## Requirements

- Define a `Book` type with title, author, page count, and checkout state.
- Define a `Library` type that stores books.
- Add operations to add a book, check out a book, return a book, and list available books.
- Create books through a constructor, factory, or validation function that rejects an empty title or negative page count.
- Keep behavior close to the type that owns the relevant data, and prevent callers from bypassing validation through direct mutation where the language permits it.

## Done when

Trying to add an invalid book, check out a missing book, or check out an already checked-out book produces a clear, intentional outcome.
