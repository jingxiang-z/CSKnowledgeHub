# Worker Pool

Build a bounded worker pool that processes independent jobs concurrently and shuts down cleanly.

## Requirements

- Accept a configurable positive worker count.
- Send jobs through a bounded queue/channel and return results through a results channel or collection.
- Process each accepted job at most once; completion order is not submission order.
- Use cancellation (`context.Context` in Go) to stop accepting work after the first fatal error.
- Wait for every owned worker before returning.
- Close channels only from their owning side and avoid sending on a closed channel.
- Add per-job timeout support as an extension.

## Tests

Test empty input, one worker, fewer jobs than workers, bounded queue behavior, deterministic failure, cancellation, and clean shutdown. Repeat tests with race analysis where available.

## Done When

The pool has no leaked workers, no blocked sends or waits, and reports completed, failed, and cancelled jobs separately.
