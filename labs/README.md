# Labs

These exercises are larger implementation tasks connected to the computer-systems notes. Each Lab documents its observable behavior, tests, and design constraints. The first supported implementations are Python and Go; C++ and Rust can be added after those versions are stable.

## Exercise Sequence

| Exercise | Primary focus | Related topics |
|---|---|---|
| [01 LRU Cache](01-lru-cache) | maps, linked data structures, and eviction | data structures, memory |
| [02 Thread-Safe TTL Cache](02-thread-safe-ttl-cache) | locks, time, cleanup, and concurrent state | operating systems |
| [03 Worker Pool](03-worker-pool) | workers, queues, cancellation, and shutdown | operating systems |
| [04 Concurrent URL Fetcher](04-concurrent-url-fetcher) | bounded concurrency, timeout, and HTTP clients | networks, concurrency |
| [05 Rate Limiter](05-rate-limiter) | synchronization, time, and API design | networks, resource limits |
| [06 Producer → Consumer Pipeline](06-producer-consumer-pipeline) | channels, backpressure, and cancellation | concurrency |
| [07 HTTP Key-Value Server](07-http-key-value-server) | HTTP, JSON, concurrent handlers, and graceful shutdown | networks, storage, concurrency |
| [08 NVML CLI](08-nvml-cli) | GPU monitoring, native-library integration, and resource lifecycle | GPU architecture, concurrency, tooling |

## Workflow

Start with one language and make the behavior correct and tested. Add the second implementation with the same external contract, while using that language's natural types, concurrency primitives, and error model. Compare implementations only where the comparison explains a meaningful systems or language trade-off.

Each Lab may contain language-specific directories, for example:

```text
02-thread-safe-ttl-cache/
├── README.md
├── python/
└── go/
```

The other exercises intentionally provide requirements rather than complete solutions. Check the individual README for the current implementation status.
