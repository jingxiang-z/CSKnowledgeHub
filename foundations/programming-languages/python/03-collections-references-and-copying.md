# 03 Collections, References, and Copying

Choose a collection by its access pattern. Assignment shares an object; it does not implicitly copy the object's contents.

## Choose a Collection

| Type | Typical use |
|---|---|
| `list` | Mutable ordered sequence |
| `tuple` | Immutable sequence, often a fixed record |
| `dict` | Mapping from hashable keys to values |
| `set` | Distinct hashable values and membership checks |

```python
titles = ["Systems notes", "Python notes"]
alias = titles
alias.append("Go notes")

copied = titles.copy()
copied[0] = "Independent title"
print(titles)

counts = {}
for title in titles:
    category = title.split()[0]
    counts[category] = counts.get(category, 0) + 1

for category, count in sorted(counts.items()):
    print(category, count)

categories = set(counts)
print("Python" in categories)
```

## Mutation and Shallow Copies

`alias` refers to the same list as `titles`; appending through either name changes that list. `copy()` creates another list, but a shallow copy still shares nested objects. A list slice such as `titles[:2]` also creates a shallow list copy. Use deliberate deep copying only when independent nested state is required.

Function arguments follow the same rules: mutating a passed list affects that list, while rebinding a parameter to another object does not rebind the caller's name. A tuple's own element references cannot change, but those elements can refer to mutable objects.

## Lookup and Ordering

List indexing raises `IndexError` outside its bounds, while slices are clipped to available bounds. `mapping[key]` raises `KeyError` for a missing key; `get` supplies a default instead. `dict` preserves insertion order, and sets have no defined iteration order. Sort explicitly when output should follow a chosen order.

Dictionary keys and set members must be hashable; lists cannot be keys. Avoid changing the size of a collection while iterating over it; construct a new result or iterate over a snapshot when needed.

[Next: Functions and Scope](04-functions-and-scope.md)

## References

- [Python tutorial: Data structures](https://docs.python.org/3/tutorial/datastructures.html)
- [Standard library: copy](https://docs.python.org/3/library/copy.html)
