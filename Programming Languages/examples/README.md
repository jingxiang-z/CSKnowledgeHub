# Programming Language Exercises

These exercises form a translation-based learning path for someone who already knows Python and C++:

```text
Python baseline → Go translation → C++ baseline → Rust translation → comparison
```

Implement the same observable behavior in all four languages, but use each language's natural types and error model. The objective is not line-by-line translation—it is learning which design decisions transfer and which must change.

## Exercise Sequence

| Exercise | Primary focus | Related chapters |
|---|---|---|
| [01 Record Analyzer](01-record-analyzer) | types, collections, control flow, and functions | 01 |
| [02 Library Catalog](02-library-catalog) | data modeling, methods, validation, and invariants | 02 |
| [03 Checkout Engine](03-checkout-model) | composition, variants, state transitions, and errors | 02, 05, 10 |
| [04 LRU Cache](04-lru-cache) | maps, ownership, linked data structures, and eviction | 03, 04 |
| [05 Thread-Safe TTL Cache](05-thread-safe-ttl-cache) | locks, time, cleanup, and concurrent state | 08 |
| [06 Worker Pool](06-worker-pool) | workers, queues, cancellation, and shutdown | 08 |
| [07 Concurrent URL Fetcher](07-concurrent-url-fetcher) | bounded concurrency, timeout, cancellation, and HTTP clients | 08, 09 |
| [08 Rate Limiter](08-rate-limiter) | synchronization, time, and API design | 08 |
| [09 Producer → Consumer Pipeline](09-producer-consumer-pipeline) | channels, backpressure, composition, and cancellation | 08 |
| [10 HTTP Key-Value Server](10-http-key-value-server) | HTTP, JSON, concurrent handlers, and graceful shutdown | 08, 09 |
| [11 NVML GPU Monitor CLI](11-nvml-cli-capstone) | native bindings, adapters, errors, testing, and tooling | 03–10 |

Chapter numbers refer to the [Programming Languages learning path](../README.md).

## Four-Pass Workflow

For each exercise:

1. **Implement the Python baseline.** Concentrate on correct behavior and tests. Record where Python relies on runtime conventions.
2. **Translate the behavior into Go.** Redesign exceptions as returned errors, classes as structs plus methods or interfaces, and implicit behavior as explicit static types.
3. **Implement the C++ baseline.** Use your existing C++ knowledge to make ownership, values, variants, and cleanup explicit.
4. **Translate the behavior into Rust.** Redesign pointer ownership, nullable states, exceptions, and inheritance using ownership, borrowing, `Option`, `Result`, enums, and traits.
5. **Complete the [comparison template](COMPARISON-TEMPLATE.md).** Explain differences in semantics and design, not merely syntax.

Finish one exercise in all four languages before starting the next. This keeps the problem familiar while the new language concept changes.

## Suggested Project Layout

Create one subdirectory per language inside each exercise, following the pattern already used by `01-record-analyzer`:

```text
03-checkout-model/
├── python-checkout-engine/
├── go-checkout-engine/
├── cpp-checkout-engine/
├── rust-checkout-engine/
└── COMPARISON.md
```

Keep equivalent behavior tests in every implementation. Exact file layouts should follow each ecosystem rather than being artificially identical.

## When to Read Existing Code

Exercise 01 includes example implementations. Attempt your own version first. Use the existing implementation only after your tests pass or when you are blocked, then write down what its design does differently. The other exercises intentionally provide requirements rather than solutions.
