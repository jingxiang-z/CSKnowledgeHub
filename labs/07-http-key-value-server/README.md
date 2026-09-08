# Mini HTTP Key-Value Server

Build a small concurrent HTTP JSON service backed by an in-memory key-value store.

## Endpoints

- `PUT /keys/{key}`: validate and store a JSON value.
- `GET /keys/{key}`: return the stored value or `404`.
- `DELETE /keys/{key}`: delete a value and return an appropriate status.
- `GET /health`: return service health.

## Requirements

- Use the language’s standard HTTP server facilities (`net/http` in Go).
- Parse and serialize JSON with useful validation errors.
- Make the backing store safe for concurrent handlers.
- Use appropriate status codes: `200`, `201`, `204`, `400`, `404`, and `405`.
- Keep routing, HTTP translation, store operations, and executable setup separate.
- Add request logging/recovery middleware.
- Shut down gracefully: stop accepting new requests, honor a shutdown context, and wait for in-flight requests within a deadline.

## Tests

Use an in-process test server. Test CRUD, malformed JSON, invalid keys, unknown routes, unsupported methods, concurrent requests, and graceful shutdown.

## Done When

The service has deterministic HTTP behavior, does not race under concurrent handlers, and can stop without abruptly abandoning active requests.
