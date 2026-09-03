# Checkout Engine

Build a small checkout engine that accepts valid orders, rejects invalid operations, and produces a receipt. This exercise combines composition, variant types, state transitions, and recoverable errors.

## Domain Model

An order contains:

- a customer with an identifier and name;
- a shipping address;
- one or more line items, each with a product name, unit price, and positive quantity;
- exactly one payment method: cash, card, or bank transfer;
- one state: draft, paid, cancelled, or shipped.

A card stores only a display-safe last-four value—never a real card number. A bank transfer stores a reference string.

## Required Operations

- Create a draft order with validated customer and address data.
- Add and remove line items while the order is still a draft.
- Calculate the subtotal and a fixed tax rate using floating-point numbers.
- Select exactly one payment method and pay the order.
- Cancel a draft or paid order, but not a shipped order.
- Ship a paid order, but reject every other invalid state transition.
- Produce a receipt containing line items, subtotal, tax, total, payment description, and final state.

Represent ordinary failures deliberately: an empty order cannot be paid, quantities must be positive, prices cannot be negative, and an operation invalid for the current state must return an error rather than partially modifying the order.

## Suggested Scenarios

Demonstrate at least these cases:

1. A valid two-item card order is paid and shipped.
2. Paying an empty order fails.
3. Adding an item after payment fails.
4. Shipping a draft order fails.
5. Cancelling a shipped order fails.

## Four-Language Focus

- **Python:** begin with dataclasses, an `Enum`, and domain-specific exceptions or explicit result objects.
- **Go:** use structs, a state type with named constants, interfaces or tagged payment data, and returned `error` values.
- **C++:** use value types, `enum class`, `std::variant`, integer minor currency units, and one consistent error strategy.
- **Rust:** use structs and enums so payment cases carry only their valid data; return `Result` from fallible transitions.

Do not force every implementation to have identical class hierarchies. Preserve the same behavior and invariants while using each language's natural representation.

## Tests

Write tests for every suggested scenario. For each failed transition, verify both the returned error and that the order remained unchanged.

## Done When

An order cannot enter an invalid normal state through its public operations, failures contain useful context, monetary calculations use the selected numeric representation, and adding a new payment variant has an obvious implementation path.
