# Notification Router

Build a notification service whose routing logic depends on behavior rather than concrete sender types. This exercise focuses on interfaces, traits, protocols, generic code, dynamic dispatch, and package boundaries.

## Domain Model

A message has an identifier, recipient, subject, body, and priority. Implement three senders that simulate delivery without using external services:

- email sender;
- SMS sender;
- console sender.

Each sender either returns a delivery receipt or a meaningful error. For example, an SMS sender can reject an empty phone number, while a configured test sender can deliberately fail.

## Requirements

- Define the smallest behavioral abstraction needed to send one message.
- Route messages by recipient preference and fall back to the console sender when the preferred sender reports a retryable failure.
- Keep sender-specific formatting out of the router.
- Store differently typed senders behind one runtime abstraction where the language requires it.
- Implement a reusable retry operation that accepts any compatible sender and a maximum attempt count.
- Inject a fake or recording sender into tests; do not add test-only branches to production routing code.
- Separate domain types, sender implementations, routing logic, and the executable entry point into sensible modules or packages.

## Four-Language Focus

- **Python:** first implement normal duck typing, then add a `Protocol` that documents the required operation.
- **Go:** define a small consumer-side interface and let sender types satisfy it implicitly.
- **C++:** implement the runtime version with an abstract base class, then compare it with a template or concept-based retry helper.
- **Rust:** use a trait bound for the generic retry helper and a trait object only where heterogeneous runtime storage is needed.

## Design Questions

Record your answers:

1. Which calls use static dispatch and which use dynamic dispatch?
2. Can a new sender be added without editing the router's core algorithm?
3. Who owns each sender while the router is using it?
4. Is the abstraction larger than any consumer actually needs?

## Tests

Test preferred delivery, retry then success, permanent failure without retry, fallback delivery, and exhausted attempts. Assert against recorded calls and receipts rather than console output.

## Done When

The router can use a new sender through the existing abstraction, test doubles require no production-code changes, and you can explain the dispatch and ownership choice in every implementation.
