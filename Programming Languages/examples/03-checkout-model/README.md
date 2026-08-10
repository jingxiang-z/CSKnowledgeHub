# Checkout Model

Model an order that has a customer, shipping address, line items, and exactly one payment method.

## Requirements

- Use composition for the customer, address, and line items.
- Represent payment as distinct cases such as cash, card, and bank transfer.
- Calculate the total from the line items.
- Avoid a model where unrelated optional fields allow several payment methods at once.

## Done when

The type design makes the valid states obvious and keeps an invalid payment combination out of normal use.
