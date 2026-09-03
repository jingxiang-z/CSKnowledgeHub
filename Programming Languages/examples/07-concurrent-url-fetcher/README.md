# Concurrent URL Fetcher

Fetch a supplied list of URLs with bounded concurrency, cancellation, and per-request error reporting.

## Requirements

- Accept up to 100 URLs and a positive concurrency limit.
- Use a worker pool or semaphore so no more than `N` requests are active.
- Apply a caller-provided context and request timeout.
- Return one result per URL containing URL, status code when available, body size, and error.
- Continue after ordinary request failures; cancel promptly when the caller cancels.
- Close response bodies on every path and avoid goroutine leaks.
- Preserve input ordering in the final result collection.

## Tests

Use a local test server, not the public internet. Test concurrency limits, timeout, cancellation, non-2xx responses, malformed URLs, partial failure, and response-body cleanup.

## Done When

The fetcher bounds active work, leaves no request or worker running after return, and gives each URL an independently useful result.
