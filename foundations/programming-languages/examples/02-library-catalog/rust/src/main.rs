use std::collections::HashMap;

pub struct Book {
    title: String,
    author: String,
    page_count: u32,
    checkout_state: bool,
}

impl Book {
    pub fn new(title: String, author: String, page_count: u32) -> Result<Self, &'static str> {
        if title.trim().is_empty() {
            return Err("Book title must not be empty");
        }

        // u32 cannot represent negative page counts.
        Ok(Self {
            title,
            author,
            page_count,
            checkout_state: false,
        })
    }

    pub fn title(&self) -> &str {
        &self.title
    }

    pub fn author(&self) -> &str {
        &self.author
    }

    pub fn page_count(&self) -> u32 {
        self.page_count
    }

    pub fn is_checked_out(&self) -> bool {
        self.checkout_state
    }

    pub fn check_out(&mut self) -> Result<(), &'static str> {
        if self.checkout_state {
            return Err("Book is already checked out");
        }

        self.checkout_state = true;
        Ok(())
    }

    pub fn return_book(&mut self) -> Result<(), &'static str> {
        if !self.checkout_state {
            return Err("Book is not checked out");
        }

        self.checkout_state = false;
        Ok(())
    }
}

pub struct Library {
    books: HashMap<String, Book>,
}

impl Library {
    pub fn new() -> Self {
        Self {
            books: HashMap::new(),
        }
    }

    pub fn add_book(&mut self, book: Book) -> Result<(), &'static str> {
        let title = book.title().to_string();
        if self.books.contains_key(&title) {
            return Err("A book with this title already exists in the library");
        }

        self.books.insert(title, book);
        Ok(())
    }

    pub fn check_out(&mut self, title: &str) -> Result<(), &'static str> {
        let book = self
            .books
            .get_mut(title)
            .ok_or("Book not found in library")?;
        book.check_out()
    }

    pub fn return_book(&mut self, title: &str) -> Result<(), &'static str> {
        let book = self
            .books
            .get_mut(title)
            .ok_or("Book not found in library")?;
        book.return_book()
    }

    pub fn available_books(&self) -> Vec<&Book> {
        let mut books: Vec<&Book> = self
            .books
            .values()
            .filter(|book| !book.is_checked_out())
            .collect();
        books.sort_by(|a, b| a.title().cmp(b.title()));
        books
    }
}

fn main() -> Result<(), &'static str> {
    let mut library = Library::new();
    let book = Book::new(
        "The Hobbit".to_string(),
        "J. R. R. Tolkien".to_string(),
        310,
    )?;
    library.add_book(book)?;

    library.check_out("The Hobbit")?;
    println!(
        "Available after checkout: {}",
        library.available_books().len()
    );

    library.return_book("The Hobbit")?;
    for book in library.available_books() {
        println!(
            "{} by {} ({} pages)",
            book.title(),
            book.author(),
            book.page_count()
        );
    }

    Ok(())
}
