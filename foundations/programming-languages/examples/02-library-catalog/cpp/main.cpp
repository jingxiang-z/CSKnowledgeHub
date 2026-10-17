#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>

class Book {
private:
    std::string title_;
    std::string author_;
    int page_count_;
    bool checkout_state_ = false;

public:
    Book(std::string title, std::string author, int page_count)
        : title_(std::move(title)), author_(std::move(author)), page_count_(page_count) {
        if (title_.empty()) {
            throw std::invalid_argument("Book title must not be empty");
        }
        if (page_count_ < 0) {
            throw std::invalid_argument("Page count must not be negative");
        }
    }

    const std::string& title() const { return title_; }
    const std::string& author() const { return author_; }
    int page_count() const { return page_count_; }
    bool is_checked_out() const { return checkout_state_; }

    void checkout() {
        if (checkout_state_) {
            throw std::logic_error("Book is already checked out");
        }
        checkout_state_ = true;
    }

    void return_book() {
        if (!checkout_state_) {
            throw std::logic_error("Book is not checked out");
        }
        checkout_state_ = false;
    }
};

class Library {
private:
    std::unordered_map<std::string, Book> books_;

    Book& find_book(const std::string& title) {
        auto it = books_.find(title);
        if (it == books_.end()) {
            throw std::out_of_range("Book does not exist");
        }
        return it->second;
    }

public:
    void add_book(const Book& book) {
        if (!books_.emplace(book.title(), book).second) {
            throw std::invalid_argument("Book already exists");
        }
    }

    void checkout_book(const std::string& title) {
        find_book(title).checkout();
    }

    void return_book(const std::string& title) {
        find_book(title).return_book();
    }

    void list_books() const {
        for (const auto& [title, book] : books_) {
            if (!book.is_checked_out()) {
                std::cout << "Title: " << title
                          << " | Author: " << book.author()
                          << " | Page Count: " << book.page_count()
                          << " | Status: Available\n";
            }
        }
    }
};

int main() {
    Library library;
    library.add_book(Book("The Great Gatsby", "F. Scott Fitzgerald", 180));
    library.add_book(Book("1984", "George Orwell", 328));

    std::cout << "Available books:\n";
    library.list_books();

    std::cout << "\nChecking out '1984':\n";
    library.checkout_book("1984");
    library.list_books();

    std::cout << "\nAttempting to check out '1984' again:\n";
    try {
        library.checkout_book("1984");
    } catch (const std::exception& error) {
        std::cout << "Error: " << error.what() << '\n';
    }

    std::cout << "\nReturning '1984':\n";
    library.return_book("1984");
    library.list_books();

    std::cout << "\nAttempting to check out a missing book:\n";
    try {
        library.checkout_book("Non-Existent Book");
    } catch (const std::exception& error) {
        std::cout << "Error: " << error.what() << '\n';
    }

    std::cout << "\nAttempting to add an invalid book:\n";
    try {
        library.add_book(Book("", "Unknown", 100));
    } catch (const std::exception& error) {
        std::cout << "Error: " << error.what() << '\n';
    }
    return 0;
}
