# Producer–Consumer

Build producers and consumers connected by one bounded buffer, using your
language's concurrency primitives.

## Requirements

- Support configurable producer and consumer counts.
- Block producers when the buffer is full and consumers when it is empty.
- On success, consume every item exactly once and stop every worker.
- On cancellation, report it and unblock all workers.
- Define who signals completion and how consumers learn no more items will arrive.

## Tests

Cover empty input, multiple producers and consumers, slow consumers,
cancellation, and shutdown. Use timeouts to catch deadlocks.

## Done When

No lost or duplicate items on success, no buffer overflow, and no stranded
workers after completion or cancellation.
