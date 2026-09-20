# Mini HTTP Key-Value Server

Build a small concurrent HTTP JSON service backed by an in-memory key-value store.

## Endpoints

- `PUT /keys/{key}`: validate and store a JSON value.
- `GET /keys/{key}`: return the stored value or `404`.
- `DELETE /keys/{key}`: delete a value and return an appropriate status.
- `GET /health`: return service health.

Keys must contain 1–128 ASCII letters, digits, underscores, or hyphens. Invalid keys return `400`.

## Requirements

- Parse and serialize JSON with useful validation errors.
- Make the backing store safe for concurrent handlers.
- Use the HTTP framework's default responses for malformed JSON and unsupported methods.
- Keep the implementation straightforward; a single file is fine.
- Log requests and return a server error for unexpected failures.
- Shut down gracefully: stop accepting new requests and allow in-flight requests to finish within a deadline.

## Tests

Use an in-process test server. Test CRUD, malformed JSON, invalid keys, unknown routes, unsupported methods, concurrent requests, and graceful shutdown.

## Done When

The service has deterministic HTTP behavior, does not race under concurrent handlers, and can stop without abruptly abandoning active requests.
