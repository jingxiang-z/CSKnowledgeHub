# 01 Getting Started and Environments

Python can evaluate code interactively or execute a script. A virtual environment gives a project its own installed packages while using a selected Python interpreter.

## Run a Script

Install Python using the [official downloads](https://www.python.org/downloads/). Check the interpreter with `python3 --version`. Save this as `main.py`:

```python
def main():
    title = "Systems notes"
    print(f"Reading: {title}")


if __name__ == "__main__":
    main()
```

Run `python3 main.py`. The `__name__` guard calls `main` when the file is run directly, while allowing another module to import its functions without starting the program. Function definitions and formatted strings appear in the next chapters.

Running `python3` without a file opens the interactive interpreter. Use `help(str)` to inspect built-in documentation and `exit()` to leave it.

## Isolate Dependencies

In a separate project directory:

```sh
python3 -m venv .venv
source .venv/bin/activate
python --version
python -m pip --version
```

After activation, `python` selects the environment's interpreter. `python -m pip` runs pip through that same interpreter. On Windows PowerShell, activation uses `.venv\Scripts\Activate.ps1`. Activation is optional when you invoke the environment's interpreter by its full path.

These chapters need no third-party packages. When a project needs one, use `python -m pip install <package>` in its environment and record dependencies in the project's chosen dependency file. A virtual environment isolates installations, but does not by itself pin versions or reproduce an environment. Keep generated environment directories out of source control.

[Next: Values and Control Flow](02-values-and-control-flow.md)

## References

- [Python tutorial: Using the interpreter](https://docs.python.org/3/tutorial/interpreter.html)
- [Python tutorial: Virtual environments and packages](https://docs.python.org/3/tutorial/venv.html)
