# `nvmlctl` — NVML GPU Monitor CLI Capstone

Build a production-style, read-only command-line tool for inspecting NVIDIA GPU state and health through the NVIDIA Management Library (NVML). Implement equivalent behavior across the languages in this learning path so the same realistic infrastructure problem exposes each language's design and error-model choices.

The goal is to practice idiomatic language design, concurrency, interface design, error handling, testing, and graceful shutdown while working with a real native-library boundary. A live integration run requires an NVIDIA GPU and driver; unit tests must use a fake provider and require no hardware.

## Features and Commands

Support commands equivalent to:

```text
nvmlctl gpu system
nvmlctl gpu list
nvmlctl gpu info 0
nvmlctl gpu health 0
nvmlctl gpu processes 0
nvmlctl gpu watch --interval 2s --count 10
nvmlctl gpu list --output json
```

`0` is an NVML index. Also support selection by UUID or PCI bus identifier where the language's CLI parser makes it practical. Support human-readable tables and JSON for `system`, `list`, `info`, and `health`.

The tool must be able to:

- list available GPUs;
- display static GPU information and dynamic metrics;
- show active compute processes and their GPU memory use;
- run basic, configurable health checks;
- watch metrics continuously with a bounded `--count` for repeatable runs;
- query multiple GPUs concurrently while keeping final output ordered by NVML index;
- respond to cancellation and shut down cleanly.

## Information to Collect

### System information

- NVIDIA driver version;
- NVML version;
- detected device count.

### Static device information

- NVML index;
- product name;
- UUID;
- PCI bus identifier.

### Dynamic device information

- GPU temperature in degrees Celsius;
- GPU and memory utilization percentages;
- total, used, and free memory in bytes;
- current power usage and enforced power limit in milliwatts;
- fan speed percentage when supported.

Keep raw units in domain values; convert only in renderers. A metric may be available, unsupported, or failed. One unsupported or failed metric must not discard the rest of a device snapshot.

## Architecture

Keep native binding calls out of commands and renderers:

```text
CLI and renderer
        │
        ▼
Service / domain layer
        │
        ▼
GPUProvider interface
        │
        ▼
NVML adapter and session
```

The adapter owns NVML initialization and shutdown exactly once per command invocation. It converts binding-specific handles and return values into domain values without exposing native handles above the adapter.

Define a narrow provider abstraction that lists devices and fetches device details, metrics, and processes. `DeviceSelector` should explicitly represent the supported selectors (index, UUID, or PCI bus ID), rather than treating every identifier as an ambiguous string. Implement a fake provider for tests.

## Health Checks

Convert raw metrics into typed health results in the domain layer:

```text
NVML → raw metrics → health rules → health results → CLI / JSON
```

Health rules should be pure functions with documented, configurable thresholds. Start with temperature and memory-pressure checks; do not silently invent values for unsupported metrics.

```json
{
  "status": "warning",
  "checks": [
    {
      "name": "temperature",
      "status": "warning",
      "value": 91,
      "message": "GPU temperature exceeds threshold"
    }
  ]
}
```

## Concurrency, Cancellation, and Lifecycle

- Use bounded concurrency when gathering information for multiple GPUs.
- Preserve deterministic result order even when device queries finish out of order.
- Use the language's cancellation mechanism to stop watch loops, queued work, and service-level waits.
- Treat cancellation as cooperative: an already-started native NVML call may finish before control returns.
- Wait for all owned work before command exit.
- Use timers/tickers without leaking them; watch mode must stop on context cancellation, count completion, or an error.
- Always release NVML resources after normal completion, cancellation, or failure.

Do not change GPU clocks, power limits, persistence mode, or any device state.

## Error Behavior

Initialization failure, an invalid selector, and a lost device must produce a nonzero exit status and readable diagnostics. For multi-GPU commands, retain successful device results when another device has a partial query failure; report the affected device and metric with useful context.

## Testing

Use a fake provider and an injected clock, ticker, or sampler. Do not make unit tests depend on real sleeps or an installed NVIDIA driver.

Cover at least:

- zero, one, and multiple GPUs;
- stable output ordering by NVML index;
- index, UUID, and PCI selector validation;
- provider initialization and query failures;
- unsupported and failed metrics alongside otherwise valid device data;
- partial device failure during concurrent collection;
- context cancellation and timeouts;
- bounded watch collection and cleanup;
- health-rule thresholds;
- exact raw JSON fields and units;
- JSON rendering and CLI exit behavior.

Run the language's normal unit-test and race-analysis tooling where available.

## Live Integration Test

On a machine with NVIDIA drivers:

1. Run `nvidia-smi` to confirm the driver can see the GPU.
2. Run `system`, `list`, and `info 0` in all four implementations.
3. Compare stable identifiers and raw units, not time-varying metric values.
4. Run a bounded `watch` while starting and stopping a GPU workload.
5. Record unsupported metrics from the actual GPU rather than manufacturing fallback values.

## Scope

This is a small, reliable systems tool—not a full monitoring platform. The initial version excludes database persistence, a Kubernetes operator, a web UI, a Prometheus server, and distributed agents.

## Done When

All four implementations pass equivalent fake-provider tests and successfully query a real GPU when available. They expose the same raw fields and units, handle partial failures without losing useful data, stop cleanly on cancellation, and keep binding-specific types behind the adapter boundary.

## References

- [NVIDIA NVML API Reference](https://docs.nvidia.com/deploy/nvml-api/nvml-api-reference.html)
- [NVIDIA Python binding distribution](https://pypi.org/project/nvidia-ml-py/)
- [nvml-wrapper for Rust](https://github.com/rust-nvml/nvml-wrapper)
