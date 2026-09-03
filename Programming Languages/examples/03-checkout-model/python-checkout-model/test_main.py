import unittest

from main import CheckoutError, Customer, Item, Order, OrderState, PaymentMethod


def new_order(items=None):
    return Order(Customer("Ada", "ada@example.com"), "1 Computing Lane", items)


class CheckoutModelTests(unittest.TestCase):
    def test_valid_two_item_card_order_is_paid_and_shipped(self):
        order = new_order([Item("Book", 12.50, 2), Item("Pen", 1.25, 1)])
        order.pay_order(PaymentMethod.CARD)
        order.ship_order()
        self.assertEqual(order.state, OrderState.SHIPPED)
        self.assertAlmostEqual(order.calculate_total(0.10), 28.87)
        self.assertIn("State: SHIPPED", order.produce_receipt(0.10))

    def test_paying_an_empty_order_fails_without_changing_it(self):
        order = new_order()
        with self.assertRaisesRegex(CheckoutError, "empty order"):
            order.pay_order(PaymentMethod.CASH)
        self.assertEqual(order.state, OrderState.DRAFT)
        self.assertIsNone(order.payment_method)

    def test_adding_an_item_after_payment_fails(self):
        order = new_order([Item("Book", 10, 1)])
        order.pay_order(PaymentMethod.CASH)
        with self.assertRaises(CheckoutError):
            order.add_item(Item("Pen", 1, 1))
        self.assertEqual(len(order.items), 1)

    def test_shipping_a_draft_order_fails(self):
        order = new_order([Item("Book", 10, 1)])
        with self.assertRaises(CheckoutError):
            order.ship_order()
        self.assertEqual(order.state, OrderState.DRAFT)

    def test_cancelling_a_shipped_order_fails(self):
        order = new_order([Item("Book", 10, 1)])
        order.pay_order(PaymentMethod.CASH)
        order.ship_order()
        with self.assertRaises(CheckoutError):
            order.cancel_order()
        self.assertEqual(order.state, OrderState.SHIPPED)


if __name__ == "__main__":
    unittest.main()
