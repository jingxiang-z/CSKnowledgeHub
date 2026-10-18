# 04 Functions and Scope

Functions give behavior a name and define an interface through their parameters. A function can return any object, including another function.

## Parameters and Return Values

```python
def passing_scores(scores, *, threshold=75):
    return [score for score in scores if score >= threshold]


def add_title(title, titles=None):
    if titles is None:
        titles = []
    titles.append(title)
    return titles


def make_labeler(prefix):
    def label(title):
        return f"{prefix}: {title}"

    return label


print(passing_scores([72, 88, 95], threshold=90))
print(add_title("Systems notes"))
label = make_labeler("Available")
print(label("Python notes"))
```

Parameters after `*` are keyword-only, so `threshold` is supplied by name. `*args` collects positional arguments and `**kwargs` collects keyword arguments when a function genuinely needs a variable argument list. A function without an explicit return value returns `None`. Returning `a, b` creates one tuple that callers can unpack.

The list comprehension above builds a new list; chapter 9 explains lazy alternatives.

## Defaults and Name Lookup

Default arguments are evaluated once when the function is defined. A default of `titles=[]` would share the same list across calls. Using `None` and creating a list inside the function avoids that accidental shared state.

Name lookup normally checks local, enclosing function, module global, and built-in scopes. Assignment inside a function normally makes a name local. `nonlocal` targets an enclosing function's binding; `global` targets a module binding. Prefer explicit parameters and return values when that makes dependencies clearer.

The nested `label` function retains access to `prefix` after `make_labeler` returns. Closures refer to captured bindings, so functions created in a loop can all observe the final loop value unless you deliberately bind separate values.

[Next: Modules and Packages](05-modules-and-packages.md)

## References

- [Python tutorial: Defining functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)
- [Python tutorial: Scopes and namespaces](https://docs.python.org/3/tutorial/classes.html#python-scopes-and-namespaces)
