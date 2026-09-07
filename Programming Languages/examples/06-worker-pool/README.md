# Worker Pool

Build a bounded worker pool that processes independent jobs concurrently and shuts down cleanly.

## Requirements

- Accept a configurable positive worker count.
- Submit jobs through a bounded work queue and collect their results.
- Process each accepted job at most once; completion order is not submission order.
- Record job failures without stopping other jobs or rejecting new submissions.
- Wait for every worker created by the pool before returning.
- Give the pool clear ownership of its queue and shutdown lifecycle; do not submit work after shutdown begins.
- Add per-job timeout support as an extension.

## Tests

Test empty input, one worker, fewer jobs than workers, bounded queue behavior, deterministic failure, cancellation, and clean shutdown. Use the language's concurrency or race-analysis tools when available.

## Done When

The pool has no leaked workers, no blocked sends or waits, and reports completed, failed, and cancelled jobs separately.
