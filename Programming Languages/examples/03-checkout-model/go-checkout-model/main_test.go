package main

import "testing"

func newTestOrder(items ...Item) *Order {
	return NewOrder(
		Customer{Name: "Ada", Email: "ada@example.com"},
		"1 Computing Lane",
		items,
	)
}

func TestOrderAddItem(t *testing.T) {
	order := newTestOrder(Item{Name: "Book", Price: 10, Quantity: 1})
	item := Item{Name: "Pen", Price: 1.25, Quantity: 2}

	if err := order.AddItem(item); err != nil {
		t.Fatalf("AddItem() error = %v, want nil", err)
	}
	if len(order.Items) != 2 {
		t.Fatalf("len(Items) = %d, want 2", len(order.Items))
	}
}

func TestValidTwoItemCardOrderIsPaidAndShipped(t *testing.T) {
	order := newTestOrder(
		Item{Name: "Book", Price: 12.50, Quantity: 2},
		Item{Name: "Pen", Price: 1.25, Quantity: 1},
	)

	if err := order.PayOrder(PaymentMethodCard); err != nil {
		t.Fatalf("PayOrder() error = %v, want nil", err)
	}
	if err := order.ShipOrder(); err != nil {
		t.Fatalf("ShipOrder() error = %v, want nil", err)
	}
	if order.State != OrderStateShipped {
		t.Fatalf("State = %q, want %q", order.State, OrderStateShipped)
	}
	if total := order.CalculateTotal(0.10); total != 28.875 {
		t.Fatalf("CalculateTotal(0.10) = %v, want 28.875", total)
	}
}

func TestPayingEmptyOrderFailsWithoutChangingIt(t *testing.T) {
	order := newTestOrder()

	if err := order.PayOrder(PaymentMethodCash); err == nil {
		t.Fatal("PayOrder() error = nil, want an error")
	}
	if order.State != OrderStateDraft {
		t.Fatalf("State = %q after failed payment, want %q", order.State, OrderStateDraft)
	}
	if order.PaymentMethod != "" {
		t.Fatalf("PaymentMethod = %q after failed payment, want empty", order.PaymentMethod)
	}
}

func TestAddingItemAfterPaymentFailsWithoutChangingItems(t *testing.T) {
	order := newTestOrder(Item{Name: "Book", Price: 10, Quantity: 1})
	if err := order.PayOrder(PaymentMethodCash); err != nil {
		t.Fatalf("PayOrder() error = %v, want nil", err)
	}

	if err := order.AddItem(Item{Name: "Pen", Price: 1, Quantity: 1}); err == nil {
		t.Fatal("AddItem() error = nil, want an error")
	}
	if len(order.Items) != 1 {
		t.Fatalf("len(Items) = %d after failed AddItem, want 1", len(order.Items))
	}
}

func TestShippingDraftOrderFailsWithoutChangingState(t *testing.T) {
	order := newTestOrder(Item{Name: "Book", Price: 10, Quantity: 1})

	if err := order.ShipOrder(); err == nil {
		t.Fatal("ShipOrder() error = nil, want an error")
	}
	if order.State != OrderStateDraft {
		t.Fatalf("State = %q after failed shipping, want %q", order.State, OrderStateDraft)
	}
}

func TestCancellingShippedOrderFailsWithoutChangingState(t *testing.T) {
	order := newTestOrder(Item{Name: "Book", Price: 10, Quantity: 1})
	if err := order.PayOrder(PaymentMethodCash); err != nil {
		t.Fatalf("PayOrder() error = %v, want nil", err)
	}
	if err := order.ShipOrder(); err != nil {
		t.Fatalf("ShipOrder() error = %v, want nil", err)
	}

	if err := order.CancelOrder(); err == nil {
		t.Fatal("CancelOrder() error = nil, want an error")
	}
	if order.State != OrderStateShipped {
		t.Fatalf("State = %q after failed cancellation, want %q", order.State, OrderStateShipped)
	}
}
