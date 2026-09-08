from enum import Enum


class CheckoutError(Exception):
    pass


class PaymentMethod(Enum):
    CASH = 1
    CARD = 2
    BANK_TRANSFER = 3


class OrderState(Enum):
    DRAFT = 1
    PAID = 2
    SHIPPED = 3
    CANCELLED = 4


class Customer:
    def __init__(self, name: str, email: str):
        if not name.strip() or not email.strip():
            raise CheckoutError("Customer name and email are required.")
        self.name = name
        self.email = email


class Item:
    def __init__(self, name: str, price: float, quantity: int):
        if not name.strip():
            raise CheckoutError("Item name is required.")
        if price < 0:
            raise CheckoutError("Price cannot be negative.")
        if quantity <= 0:
            raise CheckoutError("Quantity must be a positive integer.")
        self.name = name
        self.price = price
        self.quantity = quantity


class Order:
    def __init__(self, customer: Customer, address: str, items: list = None):
        if not address.strip():
            raise CheckoutError("Address is required.")
        self.customer = customer
        self.items = list(items) if items is not None else []
        self.address = address
        self.payment_method = None
        self.state = OrderState.DRAFT

    def add_item(self, item: Item):
        if self.state != OrderState.DRAFT:
            raise CheckoutError("Cannot add items to an order that is not in DRAFT state.")
        self.items.append(item)

    def remove_item(self, item: Item):
        if self.state != OrderState.DRAFT:
            raise CheckoutError("Cannot remove items from an order that is not in DRAFT state.")
        try:
            self.items.remove(item)
        except ValueError as error:
            raise CheckoutError("Item is not in this order.") from error

    def calculate_total(self, tax_rate=0.0):
        if tax_rate < 0:
            raise CheckoutError("Tax rate cannot be negative.")
        subtotal = sum(item.price * item.quantity for item in self.items)
        tax = round(subtotal * tax_rate, 2)
        return subtotal + tax

    def pay_order(self, payment_method: PaymentMethod):
        if self.state != OrderState.DRAFT:
            raise CheckoutError("Order can only be paid when in DRAFT state.")
        if not self.items:
            raise CheckoutError("Cannot pay an empty order.")
        if not isinstance(payment_method, PaymentMethod):
            raise CheckoutError("A valid payment method is required.")
        self.payment_method = payment_method
        self.state = OrderState.PAID

    def cancel_order(self):
        if self.state not in (OrderState.DRAFT, OrderState.PAID):
            raise CheckoutError("Only DRAFT or PAID orders can be cancelled.")
        self.state = OrderState.CANCELLED

    def ship_order(self):
        if self.state != OrderState.PAID:
            raise CheckoutError("Order can only be shipped when in PAID state.")
        self.state = OrderState.SHIPPED

    def produce_receipt(self, tax_rate=0.0):
        if self.state not in (OrderState.PAID, OrderState.SHIPPED):
            raise CheckoutError("Receipt can only be produced for PAID or SHIPPED orders.")
        subtotal = sum(item.price * item.quantity for item in self.items)
        tax = round(subtotal * tax_rate, 2)
        receipt = f"Receipt for {self.customer.name}:\nAddress: {self.address}\nItems:\n"
        for item in self.items:
            receipt += f"- {item.name}: ${item.price:.2f} x {item.quantity}\n"
        receipt += f"Subtotal: ${subtotal:.2f}\nTax: ${tax:.2f}\n"
        receipt += f"Total: ${subtotal + tax:.2f}\n"
        receipt += f"Payment Method: {self.payment_method.name}\nState: {self.state.name}\n"
        return receipt
