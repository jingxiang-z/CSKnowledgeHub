# 09 Iterators and Generators

Iteration allows the same loop syntax to traverse collections, files, and computed sequences. Generators produce values on demand and retain their position between requests.

## Build a Lazy Pipeline

```python
def passing_scores(records, threshold=75):
    for record in records:
        name, text = record.split()
        score = int(text)
        if score >= threshold:
            yield name, score


records = ["Ada 91", "Lin 63", "Sam 85"]
passing = passing_scores(records)
print(next(passing))
print(list(passing))
print(list(passing))  # Already exhausted.

labels = [f"{name}: {score}" for name, score in passing_scores(records)]
print(labels)
```

Calling a generator function creates a generator without running its body. `next` runs it until a `yield`, suspends its state, and returns the yielded value. When the body finishes, iteration ends with `StopIteration`, which a `for` loop handles automatically.

## Iterable and Iterator

An iterable can supply an iterator through `iter(value)`. An iterator supplies values through `next` and is consumed as it advances. A list can supply fresh iterators; a generator object is itself an iterator and does not restart after exhaustion.

A list comprehension materializes its results immediately. A generator expression such as `(score * 2 for score in scores)` computes them lazily. `sum`, `any`, `all`, and loops consume iterables; some stop early. Lazy processing can reduce intermediate storage but does not make the work free.

Errors inside a generator appear when iteration reaches the failing operation, not necessarily when the generator is created. The example assumes well-formed records; real input needs the validation described in chapter 6. Keep resource ownership clear when a generator reads a file and callers may stop early; a caller-owned `with` block is often easiest to reason about.

[Next: Tests and Tooling](10-tests-and-tooling.md)

## References

- [Python tutorial: Iterators](https://docs.python.org/3/tutorial/classes.html#iterators)
- [Python tutorial: Generators](https://docs.python.org/3/tutorial/classes.html#generators)
