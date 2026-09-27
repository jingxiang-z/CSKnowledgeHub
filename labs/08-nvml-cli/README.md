# `gpuinfo` — NVML GPU Inspection CLI Capstone

Build a production-style, read-only command-line tool for inspecting NVIDIA GPU state and metrics through the NVIDIA Management Library (NVML). Use any programming language with access to NVML. The requirements define observable behavior and architectural boundaries without prescribing a language, framework, or binding.

The goal is to practice API design, cancellation, interface design, error handling, testing, and graceful shutdown while working with a real native-library boundary. A live integration run requires an NVIDIA GPU and driver; unit tests must use a fake provider and require no hardware.

## Features and Commands

Support commands equivalent to:

```text
gpuinfo system
gpuinfo list
gpuinfo show 0
gpuinfo process 0
gpuinfo watch 0 --interval 2s --count 10
gpuinfo list --output json
gpuinfo watch 0 --count 2 --output json
```

`processes` is also accepted as an alias for `process`.

`0` is an NVML index. For `show`, `process`, and `watch`, accept exactly one selector: a positional nonnegative index, `--uuid UUID`, or `--pci-bus-id PCI_BUS_ID`. Support all three selector forms and reject missing or conflicting selectors. `list` queries all detected GPUs; `watch` repeatedly queries only its selected GPU. Support human-readable tables and JSON for every command. In JSON mode, `watch` emits one JSON object per sample (JSON Lines).

The tool must be able to:

- list available GPUs;
- display static GPU information and dynamic metrics;
- show active compute processes and their GPU memory use;
- watch one selected GPU continuously with a bounded `--count` for repeatable runs;
- list multiple GPUs in NVML-index order;
- respond to cancellation and shut down cleanly.

The initial backend is NVIDIA NVML; the `gpuinfo` name describes the read-only purpose and does not imply support for other GPU vendors.

## Information to Collect

### System information

- NVIDIA driver version;
- CUDA driver version supported by the installed driver;
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

Keep raw units in domain values; convert only in renderers. A metric may be available, unsupported, or failed. One unsupported or failed metric must not discard the rest of a device snapshot. JSON output must include each metric state, include a value only when available, and render errors as strings rather than native error objects.

## Architecture

Keep native binding calls out of commands and renderers:

```text
CLI and renderer
        │
        ▼
Service / domain layer
        │
        ▼
GPU provider abstraction
        │
        ▼
NVML adapter and session
```

The adapter owns one NVML session per command invocation, including all watch rounds. Initialize once and shut down exactly once after successful initialization, after all owned work has finished. It converts binding-specific handles and return values into domain values without exposing native handles above the adapter.

Define a narrow provider abstraction that lists devices and fetches device details, metrics, and processes. Represent device selectors explicitly by kind (index, UUID, or PCI bus ID), rather than treating every identifier as an ambiguous string. Implement a fake provider for tests.

## Cancellation and Lifecycle

- Preserve deterministic NVML-index order when listing devices.
- Pass cancellation through the provider abstraction and stop watch loops and service-level waits promptly.
- Treat cancellation as cooperative: an already-started native NVML call may finish before control returns. Check for cancellation before the next binding call.
- Require a positive `--interval` and, when supplied, a positive integer `--count`. Omit `--count` to watch until cancelled.
- Collect the first watch sample immediately, then wait the requested interval after each completed sample before starting the next. Do not overlap samples. Count completed samples of the selected GPU.
- Release scheduling resources when finished; watch mode must stop on cancellation, count completion, or a fatal error. Unsupported or failed individual metrics remain partial results and do not stop watch mode.
- Always release NVML resources after normal completion, cancellation, or failure.

Do not change GPU clocks, power limits, persistence mode, or any device state.

## Error Behavior

Initialization failure, an invalid selector, and a lost device must produce a nonzero exit status and readable diagnostics. These are fatal errors for watch mode. Write diagnostics to stderr so they do not corrupt JSON on stdout. For multi-GPU commands, retain successful device results when another device has a partial query failure; report the affected device and metric with useful context.

## Testing

Use a fake provider and a controllable time source or sampling mechanism. Do not make unit tests depend on real sleeps or an installed NVIDIA driver.

Cover at least:

- zero, one, and multiple GPUs;
- stable output ordering by NVML index;
- index, UUID, and PCI selector validation;
- provider initialization and query failures;
- unsupported and failed metrics alongside otherwise valid device data;
- partial device failure during device listing;
- cancellation and timeouts;
- bounded watch collection and cleanup;
- exact raw JSON fields and units;
- JSON rendering and CLI exit behavior.

Run automated unit tests and use race-detection tools where available.

## Live Integration Test

On a machine with NVIDIA drivers:

1. Run `nvidia-smi` to confirm the driver can see the GPU.
2. Run `gpuinfo system`, `gpuinfo list`, and `gpuinfo show 0`.
3. Compare stable identifiers and raw units, not time-varying metric values.
4. Run a bounded `gpuinfo watch 0` while starting and stopping a GPU workload.
5. Record unsupported metrics from the actual GPU rather than manufacturing fallback values.

## Scope

This is a small, reliable systems tool—not a full monitoring platform. The initial version excludes database persistence, a Kubernetes operator, a web UI, a Prometheus server, and distributed agents.

## Done When

The implementation passes the fake-provider tests and successfully queries a real GPU when available. It exposes the required raw fields and units, handles partial failures without losing useful data, stops cleanly on cancellation, and keeps binding-specific types behind the adapter boundary.

## Implementations

- [Go](go/): Cobra commands and the Go NVML binding.
- [Python](python/README.md): argparse commands and the Python NVML binding.

## References

- [NVIDIA NVML API Reference](https://docs.nvidia.com/deploy/nvml-api/nvml-api-reference.html)
