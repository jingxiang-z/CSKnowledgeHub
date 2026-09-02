package main

import (
	"errors"
	"fmt"
)

type Book struct {
	Title         string
	Author        string
	PageCount     int
	CheckoutState bool
}

func NewBook(title string, author string, pageCount int) (*Book, error) {
	if title == "" {
		return nil, errors.New("title cannot be empty")
	}
	if pageCount < 0 {
		return nil, errors.New("page count must be greater than or equal to zero")
	}
	return &Book{
		Title:         title,
		Author:        author,
		PageCount:     pageCount,
		CheckoutState: false,
	}, nil
}

type Library struct {
	Books map[string]*Book
}

func NewLibrary() *Library {
	return &Library{
		Books: make(map[string]*Book),
	}
}

func (l *Library) AddBook(book *Book) {
	l.Books[book.Title] = book
}

func (l *Library) CheckoutBook(title string) (*Book, error) {
	book, ok := l.Books[title]
	if !ok {
		return nil, errors.New("book not found")
	}
	if book.CheckoutState {
		return nil, errors.New("book is already checked out")
	}
	book.CheckoutState = true
	return book, nil
}

func (l *Library) ReturnBook(title string) (*Book, error) {
	book, ok := l.Books[title]
	if !ok {
		return nil, errors.New("book not found")
	}
	if !book.CheckoutState {
		return nil, errors.New("book is not checked out")
	}
	book.CheckoutState = false
	return book, nil
}

func (l *Library) ListBooks() {
	for _, book := range l.Books {
		state := "available"
		if book.CheckoutState {
			state = "checked out"
		}
		fmt.Printf("Title: %s, Author: %s, Pages: %d, State: %s\n", book.Title, book.Author, book.PageCount, state)
	}
}

func main() {
	library := NewLibrary()

	book1, err := NewBook("The Great Gatsby", "F. Scott Fitzgerald", 180)
	if err != nil {
		fmt.Println(err)
		return
	}
	library.AddBook(book1)

	book2, err := NewBook("1984", "George Orwell", 328)
	if err != nil {
		fmt.Println(err)
		return
	}
	library.AddBook(book2)

	library.ListBooks()

	checkedOutBook, err := library.CheckoutBook("1984")
	if err != nil {
		fmt.Println(err)
	} else {
		fmt.Printf("Checked out: %s\n", checkedOutBook.Title)
	}

	library.ListBooks()

	returnedBook, err := library.ReturnBook("1984")
	if err != nil {
		fmt.Println(err)
	} else {
		fmt.Printf("Returned: %s\n", returnedBook.Title)
	}

	library.ListBooks()
}
