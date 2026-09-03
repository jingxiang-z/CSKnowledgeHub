# Producer → Consumer Pipeline

Build a multi-stage concurrent pipeline that consumes input, transforms it, and aggregates a summary.

## Requirements

- Model `input → transform → aggregate` as distinct stages connected by bounded channels/queues.
- Allow multiple transform workers while retaining a clear ownership rule for each channel.
- Propagate cancellation through all stages.
- Stop producers when downstream stages fail or the caller cancels.
- Close every channel exactly once from its sending owner.
- Avoid unbounded buffering; make backpressure observable.
- Return an aggregate result plus meaningful stage errors.

## Tests

Test empty input, normal transformation, transform failure, aggregate failure, cancellation, a slow consumer, and worker shutdown. Include a test that would hang if a channel is closed or drained incorrectly.

## Done When

Every stage exits on success, error, or cancellation, and no goroutine/thread is left waiting on a channel/queue.
