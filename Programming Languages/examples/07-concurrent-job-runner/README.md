# Concurrent Job Runner

Build a bounded worker pool that processes independent jobs concurrently and shuts down cleanly. This exercise focuses on threads or tasks, message passing, shared-state protection, cancellation, and nondeterministic completion order.

## Job Model

Each job has an identifier and an integer input. Its handler performs a deterministic calculation and returns either a result or an error. Configure one known job identifier to fail so cancellation and cleanup can be tested without relying on random behavior or an external service.

## Requirements

- Accept a configurable positive worker count.
- Feed jobs through a bounded queue or channel so a fast producer cannot allocate without limit.
- Process each accepted job at most once.
- Return each result with its job identifier; never assume completion order matches submission order.
- On the first fatal job error, signal cancellation, stop accepting work, and let active workers exit safely.
- Distinguish completed, failed, and cancelled jobs in the final summary.
- Wait for every owned worker before the main operation returns.
- Avoid unsynchronized shared mutation and avoid holding locks while executing the job handler.

Do not use real network requests. If you simulate latency, keep it short and place it behind an injected handler so tests do not depend on wall-clock timing.

## Four-Language Focus

- **Python:** begin with `queue.Queue` and `threading`, or use an executor while still explaining queue bounds and cancellation limits.
- **Go:** use goroutines, channels, a `WaitGroup`, and a `context.Context` or cancellation channel.
- **C++:** use `std::jthread` where available, a mutex/condition-variable queue, and cooperative stop requests.
- **Rust:** begin with scoped or owned standard threads, channels, and `Arc` only for state that truly must be shared.

Implement the threaded version before exploring an async runtime. The central lesson is task lifetime and coordination, not a particular framework.

## Tests

Test empty input, one worker, fewer jobs than workers, deterministic failure, cancellation, and a queue smaller than the job count. Run the language's race-analysis tooling where available and repeat the test suite enough times to expose ordering assumptions.

## Investigation

Answer these questions in your comparison notes:

1. Who owns the queue and cancellation signal?
2. What wakes a worker during shutdown?
3. Can any send, receive, or wait block forever?
4. Which result ordering is guaranteed?
5. What prevents a worker from outliving the operation that created it?

## Done When

The runner completes successfully without leaked workers, stops cleanly after the deliberate failure, uses bounded buffering, and produces correct summaries regardless of completion order.
