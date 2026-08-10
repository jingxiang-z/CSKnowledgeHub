# Data Access Semantics

Write a compact experiment that compares copying, aliasing, mutation, and views over a nested collection.

## Requirements

- Create a nested collection, assign it to a second name, mutate a nested value, and record what each name observes.
- Create an independent copy and repeat the mutation; identify whether it is shallow or deep.
- In Rust or C++, also demonstrate a move and state what may be used afterward.
- Implement one read-only operation and one operation that visibly modifies caller-provided state; state whether each receives a value, reference, pointer, borrow, or object binding.
- Select a middle range without unnecessarily copying the full sequence, then determine whether changing it changes the original.
- Document what source data must remain valid while the selected range/view is in use.

## Done when

The code and output explain whether each operation copies, moves, aliases, borrows, or views data, including the lifetime of any non-owning access.
