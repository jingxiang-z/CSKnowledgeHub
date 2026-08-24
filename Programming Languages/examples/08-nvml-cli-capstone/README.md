# NVML GPU Monitor CLI Capstone

Build a read-only command-line GPU monitor using the NVIDIA Management Library (NVML). Implement the same behavior in Python, Go, C++, and Rust so you can compare a Python binding, a Go binding, the native C API from C++, and a safe Rust wrapper over that API.

This project requires an NVIDIA GPU and driver for its live integration run. Unit tests must still use a fake provider so most behavior can be tested without querying real hardware.

## Commands

Support commands equivalent to:

```text
gpu-monitor system
gpu-monitor list
gpu-monitor show --index 0
gpu-monitor watch --index 0 --interval 1s --count 10
```

Also support `--format table` and `--format json` for `system`, `list`, and `show`. Exact option syntax may follow each language's CLI ecosystem, but command behavior and output fields should remain equivalent.

## Information to Collect

### System Information

- NVIDIA driver version;
- NVML version;
- detected device count.

### Static Device Information

- NVML index;
- product name;
- UUID;
- PCI bus identifier.

### Dynamic Device Information

- GPU temperature in degrees Celsius;
- GPU and memory utilization percentages;
- total, used, and free device memory in bytes;
- current power usage and enforced power limit in milliwatts;
- fan speed percentage when supported.

Do not fail the entire device query because one metric returns `NOT_SUPPORTED`. Represent each metric as available, unsupported, or failed, and retain useful error context. Initialization failure, a missing GPU index, and a lost device should produce nonzero exit statuses and readable diagnostics.

## Architecture

Separate the project into four concerns:

1. **NVML adapter:** initializes NVML, converts native return values, enumerates devices, and shuts NVML down correctly.
2. **Domain snapshot:** language-native structs/classes representing system, device, and metric data without exposing binding-specific handles.
3. **Application service:** implements list, show, and bounded watch behavior through a provider abstraction.
4. **CLI and renderer:** parses arguments and renders table or JSON output without making NVML calls directly.

Define a narrow `GpuProvider`-style abstraction that can be implemented by both the real NVML adapter and an in-memory fake. Do not distribute binding calls throughout the CLI.

## Lifecycle and Safety

- Initialize NVML exactly once for one CLI invocation and always perform the corresponding cleanup.
- Treat device handles and borrowed native data according to the selected binding's lifetime rules.
- Keep all commands read-only; do not change clocks, power limits, persistence mode, or device state.
- Give `watch` a finite `--count` for repeatable runs and release resources after normal completion or an error.
- Convert byte counts and milliwatts only in the renderer; retain raw units in the domain snapshot.

## Four-Pass Milestones

### Python Baseline

Use the `nvidia-ml-py` distribution and its `pynvml` module. Establish command behavior, snapshot types, per-metric error handling, fake-provider tests, and JSON output.

### Go Translation

Use NVIDIA's `go-nvml` bindings. Translate Python exceptions into explicit NVML return checks and Go errors. Define the provider interface beside the application code that consumes it. Note that NVIDIA's binding currently targets Linux.

### C++ Baseline

Call the native C API from `<nvml.h>` and link against NVML. Wrap initialization and shutdown in an RAII session object, translate `nvmlReturn_t` consistently, and prevent native handles from escaping the adapter unnecessarily.

### Rust Translation

Use the `nvml-wrapper` crate. Map wrapper errors into application errors, keep native lifetimes inside the adapter, and use enums or result types to distinguish available, unsupported, and failed metrics without pervasive cloning.

## Testing

### Unit Tests Without Hardware

Use a fake provider to test:

- zero, one, and multiple GPUs;
- stable ordering by NVML index;
- invalid device selection;
- one unsupported metric among otherwise valid data;
- provider initialization and query failures;
- exact raw JSON fields and units;
- bounded watch collection using an injected clock or sampler rather than real sleeps.

### Live Integration Test

On your NVIDIA machine:

1. Run `nvidia-smi` to confirm the driver can see the GPU.
2. Run `system`, `list`, and `show --index 0` in all four implementations.
3. Compare stable identifiers and raw units across implementations.
4. Run a bounded `watch` while starting and stopping a GPU workload, then observe utilization and memory changes.
5. Record which metrics your GPU reports as unsupported; do not manufacture fallback values.

Values sampled at different times need not be identical. Compare units, ranges, identifiers, and error behavior rather than requiring dynamic readings to match exactly.

## Optional Extensions

- Show active compute processes and their GPU memory use.
- Select a device by UUID or PCI bus identifier.
- Add CSV or newline-delimited JSON output for watch mode.
- Add thresholds that produce a warning exit status for temperature or memory use.
- Query multiple GPUs concurrently, then preserve deterministic output ordering.
- Compare the CLI output with a selected subset of `nvidia-smi --query-gpu` fields.

## Done When

All four implementations pass equivalent fake-provider tests and successfully query your NVIDIA GPU. They expose the same raw fields and units, handle unsupported metrics without losing the rest of a snapshot, clean up NVML on every path, and keep binding-specific types behind the adapter boundary.

## References

- [NVIDIA NVML API Reference](https://docs.nvidia.com/deploy/nvml-api/nvml-api-reference.html)
- [NVIDIA go-nvml bindings](https://github.com/NVIDIA/go-nvml)
- [NVIDIA Python binding distribution](https://pypi.org/project/nvidia-ml-py/)
- [nvml-wrapper for Rust](https://github.com/rust-nvml/nvml-wrapper)
