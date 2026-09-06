# Thread-Safe TTL Cache

Build a concurrent in-memory cache whose entries expire after a configurable
time-to-live (TTL). This exercise focuses on synchronization, clock injection,
expiration semantics, and clean background-worker shutdown.

## API

Implement the following operations using the naming conventions of your
language:

| Operation | Behavior |
| --- | --- |
| `Get(key)` | Return the live value and a found/not-found result. Treat an expired entry as a miss and remove it. |
| `Set(key, value, ttl)` | Insert or overwrite an entry with a new expiration time. Reject a non-positive TTL. |
| `Delete(key)` | Remove the entry if it exists. Deleting a missing key is a no-op. |
| `Len()` | Return the number of live entries. Expired entries must not be counted. |
| `Close()` | Stop the cleanup worker and wait for it to exit. Calling `Close` more than once should be safe. |

Returning a separate found/not-found result from `Get` is preferable to using a
sentinel value because a cached value may itself be `null`, `nil`, or `None`.

## Requirements

- Protect every access to shared cache state with an appropriate synchronization
  primitive.
- Use a readers-writer lock when the language provides one and it fits the
  design; otherwise, use a mutex or equivalent.
- Never return an expired value, even if the background cleanup worker has not
  run yet.
- Support an optional cleanup worker that periodically removes expired entries.
- Ensure the cleanup worker cannot outlive the cache that owns it.
- Inject the clock used for expiration checks so tests remain deterministic.

## Design Notes

Store each value together with its expiration timestamp. All expiration checks
must use the same injected clock.

`Get` may appear read-only, but it removes expired entries and therefore may
need exclusive access. If the implementation first checks under a read lock and
then acquires a write lock, it must check the entry again after acquiring the
write lock.

The cleanup worker is an optimization for reclaiming memory; correctness must
not depend on when it runs. Use an explicit stop signal and wait for the worker
to finish during `Close`.

## Tests

Cover the following behavior:

- cache hits and misses
- expiration and removal on access
- overwrite with a new value and TTL
- deletion of present and missing keys
- live-entry length reporting
- background cleanup
- concurrent readers
- concurrent writers
- mixed concurrent reads and writes

Use a fake clock or an explicit cleanup trigger instead of real-time sleeps.
Run the language's race detector, thread sanitizer, or equivalent concurrency
tooling when available.

## Done When

- Concurrent callers cannot observe data races or inconsistent state.
- Expired values are never returned or included in `Len()`.
- Expired entries are eventually removed.
- Cache operations remain correct under concurrent access.
- The cleanup worker stops before cache shutdown completes.
