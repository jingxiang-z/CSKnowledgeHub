# Log Analysis Pipeline

Build a lazy or streaming pipeline that parses application logs, filters events, transforms them, and computes a summary. This exercise focuses on first-class functions, closures, iterators, generators, and explicit side effects.

## Input

Each input line uses this format:

```text
2026-08-23T10:15:00Z|ERROR|payments|request-17|card declined
```

The fields are timestamp, severity, component, request identifier, and message. Include malformed lines in the sample input.

## Requirements

- Parse one line into a validated event or a recoverable parse error.
- Consume lines one at a time rather than loading every parsed event into an intermediate collection.
- Accept a predicate or closure that selects events by severity and component.
- Normalize messages with a transformation function.
- Count malformed lines without stopping the entire pipeline.
- Produce counts by severity and component, plus the first five matching request identifiers.
- Support early termination once a configurable match limit is reached.
- Keep parsing and transformation functions free of logging or hidden global mutation.

Generate at least 100,000 deterministic input lines for one run. You do not need to save them to disk; a generator or producer function is acceptable.

## Four-Language Focus

- **Python:** use a generator, generator expression, or iterator pipeline and show where evaluation actually occurs.
- **Go:** write the clear loop first; optionally express the producer as an iterator function or channel, then compare its clarity and overhead.
- **C++:** use standard algorithms or ranges and avoid dangling views captured from temporary data.
- **Rust:** compose iterator adapters and use a consuming operation such as `fold`, `collect`, or a loop for the final aggregation.

Do not force `map` and `filter` into code where an ordinary loop communicates state and failure more clearly.

## Tests

Test parsing, malformed input, predicate capture, aggregation, early termination, empty input, and the distinction between constructing a lazy pipeline and consuming it.

## Done When

The pipeline can process the large generated input with bounded intermediate memory, its filtering behavior can be changed by passing a function value, and side effects occur only at explicit consumption/reporting boundaries.
