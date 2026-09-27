# Python `gpuinfo`

A synchronous Python CLI inspired by the [GPU inspection lab](../README.md),
using standard `argparse` and NVIDIA's `nvidia-ml-py` binding (imported as
`pynvml`). Requires Python 3.11+ and an NVIDIA driver for live queries.

From this directory:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/gpuinfo system
.venv/bin/gpuinfo list
.venv/bin/gpuinfo show 0
.venv/bin/gpuinfo process 0
.venv/bin/gpuinfo watch 0 --interval 2 --count 10
.venv/bin/gpuinfo show --uuid GPU-YOUR-UUID --output json
.venv/bin/gpuinfo watch --pci-bus-id 00000000:01:00.0 --count 2 --output json
```

You can also run `python3 -m gpuinfo` from this directory. `processes` aliases
`process`, and `--output table|json` works before or after the command. Intervals
are seconds, such as `0.5`, `2`, or `90`.

The first watch sample is immediate. Later samples start after the interval has
elapsed following the previous completed sample. Watch JSON is JSON Lines, one
object per sample. Partial metric failures appear in the result and produce
stderr diagnostics; they do not stop watch. Unsupported metrics have no invented
fallback value. Other commands return status 1 for query or cleanup failures,
and invalid arguments return status 2 with argparse's standard usage message.
Ctrl+C raises `KeyboardInterrupt`; the NVML context manager runs cleanup and
the CLI returns status 130 without a traceback. A small SIGTERM handler raises
`SystemExit(143)`, which also unwinds the context manager. Native calls may delay
signal handling until they return.

## Structure

- `gpu.py`: dataclasses, metric states, explicit selectors, and a provider protocol.
- `nvml.py`: `open_session()` context manager, native queries, and conversion into domain values.
- `cli.py`: argument validation, command orchestration, and signal handling.
- `render.py`: table and JSON translation, preserving raw units and available zero values.
- `errors.py`: domain errors and aggregation of partial query failures.

Each command owns one session through a `with` block, including the entire watch
loop:

```python
with open_session() as provider:
    execute(args, provider, selector, stdout, stderr, time.sleep)
```

The context manager initializes NVML before yielding the provider and shuts it
down in `finally`. Watch uses `time.sleep()` between completed samples; exceptions
unwind the call stack and trigger cleanup. There is no cancellation token or
custom deadline mechanism. Commands and renderers consume domain values rather
than native handles. Tests inject a fake context manager and sleep function.

## Tests

From this directory, no binding installation or GPU is needed:

```sh
python3 -m unittest discover -v
```

Tests cover command validation, selectors, partial results, metric states and
units, ordering, lifecycle failures, KeyboardInterrupt/SystemExit cleanup, bounded watch,
and adapter conversion through a fake native binding.

For live verification, compare identifiers against `nvidia-smi`, run all five
commands, and use a bounded watch while starting/stopping a GPU workload. The
unit suite never starts a workload or queries real hardware.

## Live verification (2026-09-26)

Verified all five commands on an NVIDIA GeForce RTX 4080 SUPER under WSL.
The name, UUID, and PCI bus ID matched `nvidia-smi`. Total memory was
17,171,480,576 bytes, matching its reported 16,376 MiB. The installed driver
reported CUDA driver compatibility 13.2.

An eight-sample watch observed memory usage increase and decrease during a
transient 256 MiB CUDA allocation. The process command detected the workload
PID; its per-process GPU-memory metric was genuinely unsupported on this
system and was exported as `{"state":"unsupported"}`. All snapshot metrics
were available. Ctrl+C interrupted a watch waiting on a one-hour interval in
approximately 10 ms in the original implementation. After the Python-native
refactor, SIGINT and SIGTERM were rechecked against a long sleep and returned
status 130 and 143 respectively, with no traceback.
