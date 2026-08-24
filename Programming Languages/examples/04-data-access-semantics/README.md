# Message Buffer Lab

Implement a small binary-message editor that makes copying, aliasing, mutation, moves, slices, and views visible. Use an in-memory byte sequence so the same experiment works naturally in all four languages.

## Message Format

Use this simple layout:

```text
+--------+--------+-------------------+----------+
| version| flags  | UTF-8 payload     | checksum |
| 1 byte | 1 byte | variable length   | 1 byte   |
+--------+--------+-------------------+----------+
```

The checksum is the sum of every preceding byte modulo 256. Start with a valid message whose payload is ASCII text so in-place case conversion does not change its byte length.

## Required Operations

- Parse and expose the version, flags, payload range, and checksum without copying the full buffer.
- Create an independent snapshot of the complete message.
- Create a payload view, change lowercase ASCII bytes to uppercase through that view, and recompute the checksum.
- Show whether the original buffer, payload view, and snapshot observe the mutation.
- Implement a read-only checksum function and an in-place payload-normalization function.
- Reject a message shorter than three bytes and reject an invalid checksum.
- Attempt to append data while a view exists, then document what the language permits and what can become invalid.
- In C++ and Rust, move ownership of the complete buffer into another value and document what can legally be used afterward.

## Four-Language Focus

| Language | Owning buffer | Non-owning payload access | Independent copy |
|---|---|---|---|
| Python | `bytearray` | `memoryview` | `bytearray(buffer)` |
| Go | `[]byte` | subslice | `bytes.Clone` or explicit copy |
| C++ | `std::vector<std::byte>` or `std::vector<uint8_t>` | `std::span` | vector copy |
| Rust | `Vec<u8>` | `&[u8]` or `&mut [u8]` | `.clone()` |

Explain the consequences rather than merely showing syntax. In particular, identify who owns the bytes, whether a view can mutate them, what keeps them alive, and which operation could invalidate a view.

## Tests

Test valid parsing, invalid length, invalid checksum, payload mutation, snapshot independence, and an empty payload. Where the language prevents an invalid operation at compile time, preserve the rejected example as a comment and explain the diagnostic.

## Done When

The output and tests demonstrate the difference between an owner, an alias, a borrowed/viewed range, and an independent copy. Your notes must explain why each observed mutation or compiler rejection occurred.
