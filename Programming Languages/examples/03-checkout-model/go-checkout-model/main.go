package main

import (
	"fmt"
	"slices"
	"strings"
)

type PaymentMethod string

const (
	PaymentMethodCash         PaymentMethod = "cash"
	PaymentMethodCard         PaymentMethod = "card"
	PaymentMethodBankTransfer PaymentMethod = "bank_transfer"
)

type OrderState string

const (
	OrderStateDraft     OrderState = "draft"
	OrderStatePaid      OrderState = "paid"
	OrderStateCancelled OrderState = "cancelled"
	OrderStateShipped   OrderState = "shipped"
)

type Customer struct {
	Name  string
	Email string
}

type Item struct {
	Name     string
	Price    float64
	Quantity int
}

type Order struct {
	Customer      Customer
	Address       string
	Items         []Item
	PaymentMethod PaymentMethod
	State         OrderState
}

func NewOrder(customer Customer, address string, items []Item) *Order {
	return &Order{
		Customer: customer,
		Address:  address,
		Items:    slices.Clone(items),
		State:    OrderStateDraft,
	}
}

func (o *Order) AddItem(item Item) error {
	if o.State != OrderStateDraft {
		return fmt.Errorf("order is not in draft state")
	}
	if err := validateItem(item); err != nil {
		return err
	}
	o.Items = append(o.Items, item)
	return nil
}

func (o *Order) RemoveItem(item Item) error {
	if o.State != OrderStateDraft {
		return fmt.Errorf("order is not in draft state")
	}
	for i, orderItem := range o.Items {
		if orderItem == item {
			o.Items = append(o.Items[:i], o.Items[i+1:]...)
			return nil
		}
	}
	return fmt.Errorf("item %q is not in this order", item.Name)
}

func (o *Order) CalculateTotal(taxRate float64) float64 {
	total := o.subtotal()
	return total + total*taxRate
}

func (o *Order) PayOrder(paymentMethod PaymentMethod) error {
	if o.State != OrderStateDraft {
		return fmt.Errorf("order is not in draft state")
	}
	if len(o.Items) == 0 {
		return fmt.Errorf("cannot pay an empty order")
	}
	for _, item := range o.Items {
		if err := validateItem(item); err != nil {
			return err
		}
	}
	if !isValidPaymentMethod(paymentMethod) {
		return fmt.Errorf("a valid payment method is required")
	}
	o.PaymentMethod = paymentMethod
	o.State = OrderStatePaid
	return nil
}

func (o *Order) CancelOrder() error {
	if o.State != OrderStateDraft && o.State != OrderStatePaid {
		return fmt.Errorf("order is not in draft or paid state")
	}
	o.State = OrderStateCancelled
	return nil
}

func (o *Order) ShipOrder() error {
	if o.State != OrderStatePaid {
		return fmt.Errorf("order is not in paid state")
	}
	o.State = OrderStateShipped
	return nil
}

func (o *Order) ProduceReceipt() {
	subtotal := o.subtotal()
	tax := subtotal * 0.1
	for i, item := range o.Items {
		fmt.Printf("%d. %s - $%.2f x %d\n", i+1, item.Name, item.Price, item.Quantity)
	}
	fmt.Printf("Subtotal: $%.2f\n", subtotal)
	fmt.Printf("Tax: $%.2f\n", tax)
	fmt.Printf("Total: $%.2f\n", subtotal+tax)
	fmt.Printf("Payment Method: %s\n", o.PaymentMethod)
	fmt.Printf("Final State: %s\n", o.State)
}

func (o *Order) subtotal() float64 {
	total := 0.0
	for _, item := range o.Items {
		total += item.Price * float64(item.Quantity)
	}
	return total
}

func validateItem(item Item) error {
	if strings.TrimSpace(item.Name) == "" {
		return fmt.Errorf("item name is required")
	}
	if item.Price < 0 {
		return fmt.Errorf("item price cannot be negative")
	}
	if item.Quantity <= 0 {
		return fmt.Errorf("item quantity must be positive")
	}
	return nil
}

func isValidPaymentMethod(paymentMethod PaymentMethod) bool {
	return paymentMethod == PaymentMethodCash ||
		paymentMethod == PaymentMethodCard ||
		paymentMethod == PaymentMethodBankTransfer
}

func main() {
	customer := Customer{Name: "John Doe", Email: "john.doe@example.com"}
	order := NewOrder(customer, "123 Main St", []Item{
		{Name: "Product 1", Price: 10.0, Quantity: 2},
		{Name: "Product 2", Price: 15.0, Quantity: 1},
	})
	if err := order.PayOrder(PaymentMethodCard); err != nil {
		panic(err)
	}
	if err := order.ShipOrder(); err != nil {
		panic(err)
	}
	order.ProduceReceipt()
}
