class Book:
    def __init__(self, title, author, page_count, checkout_state=False):
        if not title or page_count <= 0:
            raise ValueError("Invalid book details")
        self.title = title
        self.author = author
        self.page_count = page_count
        self.checkout_state = checkout_state

class Library:
    def __init__(self):
        self.books = {}

    def add_book(self, book):
        self.books[book.title] = book

    def checkout_book(self, title):
        if title not in self.books:
            raise ValueError("Book not found in the library")
        book = self.books[title]
        if book.checkout_state:
            raise ValueError("Book is already checked out")
        book.checkout_state = True
        return book

    def return_book(self, title):
        if title not in self.books:
            raise ValueError("Book not found in the library")
        book = self.books[title]
        if not book.checkout_state:
            raise ValueError("Book is not checked out")
        book.checkout_state = False
        return book

    def list_books(self):
        for title, book in self.books.items():
            status = "Checked out" if book.checkout_state else "Available"
            print(f"{title} by {book.author}, {book.page_count} pages - {status}")

if __name__ == "__main__":
    library = Library()
    book1 = Book("The Great Gatsby", "F. Scott Fitzgerald", 180)
    book2 = Book("1984", "George Orwell", 328)
    book3 = Book("To Kill a Mockingbird", "Harper Lee", 281)

    library.add_book(book1)
    library.add_book(book2)
    library.add_book(book3)

    print("Library Catalog:")
    library.list_books()

    print("\nChecking out '1984':")
    library.checkout_book("1984")
    library.list_books()

    print("\nReturning '1984':")
    library.return_book("1984")
    library.list_books()

    print("\nAttempting to checkout a non-existent book:")
    try:
        library.checkout_book("Non-Existent Book")
    except ValueError as e:
        print(f"Error: {e}")