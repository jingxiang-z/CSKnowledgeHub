# Python implementation

From this directory, install the dependencies and run the server:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python main.py
```

The server listens on `127.0.0.1:8000`. It uses one worker because its in-memory store is local to the process. Shutdown allows active requests up to five seconds to finish.

Run the HTTP and shutdown tests with:

```sh
.venv/bin/python -m pytest -q
```
