# LRU Cache

Build an in-memory fixed-capacity cache with least-recently-used eviction. This exercise focuses on the relationship between a hash map and an ownership-linked recency list.

## Requirements

- Implement `Get(key)`, `Put(key, value)`, `Delete(key)`, `Len()`, and `Capacity()`.
- `Get` returns a found/not-found result and promotes the entry to most-recently used.
- `Put` updates an existing key without increasing the length.
- When full, `Put` evicts exactly the least-recently-used key.
- Keep map and list updates consistent; do not scan the list to find a key.
- Reject a non-positive capacity.

## Design

Use a map from key to list node plus a doubly linked list ordered most-recent to least-recent. Explain node ownership and removal in each language. Prefer a standard-library linked-list type only if its ownership and API make the invariants clear.

## Tests

Test insert/get, promotion after `Get`, promotion after an update, capacity eviction, delete, zero capacity rejection, and repeated operations on one key.

## Done When

Every public operation is O(1) on average, eviction is deterministic, and tests can inspect the recency order without relying on implementation accidents.
