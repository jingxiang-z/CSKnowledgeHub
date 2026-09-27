# Python `gpuinfo`

A synchronous Python CLI for the [GPU inspection lab](../README.md), using
`argparse` and NVIDIA's `nvidia-ml-py` binding. Requires Python 3.11+ and an
NVIDIA driver for live queries.

Run from this directory:

```sh
uv sync
uv run gpuinfo system
uv run gpuinfo list
uv run gpuinfo show 0
uv run gpuinfo process 0
uv run gpuinfo watch 0 --interval 2 --count 10
uv run gpuinfo show --uuid GPU-YOUR-UUID --output json
uv run gpuinfo watch --pci-bus-id 00000000:01:00.0 --count 2 --output json
```

Intervals are in seconds. `processes` aliases `process`. Every command supports
`--output table|json`; watch emits JSON Lines. Watch samples immediately, then
waits after each completed sample. Partial metric failures do not stop watch.

Each command owns one NVML session through a context manager. Ctrl+C and SIGTERM
run cleanup and exit with status 130 and 143 respectively. Query or cleanup
failures exit 1; invalid arguments exit 2.

## Structure

- `gpu.py`: data models and provider protocol.
- `nvml.py`: native queries and session context manager.
- `cli.py`: arguments, command orchestration, and watch loop.
- `render.py`: tables and JSON.
- `errors.py`: domain errors and partial-failure aggregation.

## Tests

```sh
uv run python -m unittest discover -v
```

Tests use fake providers and bindings; no driver or GPU is needed.

Live verification on an RTX 4080 SUPER under WSL confirmed identifiers against
`nvidia-smi`, workload memory changes, and signal shutdown. Snapshot metrics were
available; per-process GPU memory was unsupported and rendered without a
fallback value.
