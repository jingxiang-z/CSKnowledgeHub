# Thread-Safe TTL Cache

Build a concurrent in-memory cache whose entries expire after a time-to-live. This exercise focuses on synchronization, clocks, cleanup lifetimes, and predictable concurrent APIs.

## Requirements

- Store `map[string]Value` entries with an expiration time.
- Implement `Get`, `Set(key, value, ttl)`, `Delete`, and `Len`.
- A `Get` on an expired item behaves as a miss and removes the item.
- Protect every map access with an appropriate lock (`sync.RWMutex` in Go).
- Reject non-positive TTL values.
- Support an optional cleanup worker/goroutine; it must stop cleanly.
- Inject a clock or cleanup trigger in tests—do not rely on real sleeps.

## Tests

Test hits, misses, expiry, overwrite, deletion, cleanup, shutdown, and concurrent readers/writers. Run the language’s race tooling where available.

## Done When

Concurrent callers cannot observe map races, expired values are never returned, and an optional cleanup worker cannot outlive the cache that owns it.
