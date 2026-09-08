# Rate Limiter

Build a concurrency-safe rate limiter with a small, explicit `Allow` API.

## Requirements

- Implement either a token bucket or sliding-window algorithm; document the choice.
- Expose `Allow() bool` and a constructor that validates capacity and refill/window settings.
- Make calls safe from multiple concurrent callers.
- Inject a clock so tests do not sleep.
- Define behavior at the exact refill/window boundary.
- Add optional per-key/user limiting only after the single shared limiter is correct.

## Tests

Test initial capacity, exhaustion, refill/window expiry, boundary behavior, invalid configuration, and simultaneous callers. Run race analysis where available.

## Done When

The limiter admits no more requests than its documented policy allows and remains correct under concurrent calls.
