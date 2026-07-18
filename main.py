import sqlite3

DB_PATH = "database/books.db"


def connect_db():
    return sqlite3.connect(DB_PATH)


def view_books():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT BookID, Book, AuthorID, Avg_Rating
    FROM Books
    LIMIT 10;
    """)

    books = cursor.fetchall()

    print("\n--- First 10 Books ---")
    for book in books:
        print(book)

    conn.close()


def search_by_author():
    author_name = input("Enter author name: ")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT Books.Book, Author.AuthorName, Books.Avg_Rating
    FROM Books
    JOIN Author
    ON Books.AuthorID = Author.AuthorID
    WHERE Author.AuthorName = ?
    ORDER BY Books.Avg_Rating DESC;
    """, (author_name,))

    results = cursor.fetchall()

    print("\n--- Search Results ---")
    if results:
        for row in results:
            print(row)
    else:
        print("No books found for that author.")

    conn.close()


def add_book():
    book_title = input("Enter book title: ")
    author_id = input("Enter AuthorID: ")
    rating = input("Enter average rating: ")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(BookID) FROM Books;")
    max_id = cursor.fetchone()[0]

    if max_id is None:
        new_book_id = 1
    else:
        new_book_id = max_id + 1

    cursor.execute("""
    INSERT INTO Books (BookID, Book, AuthorID, Avg_Rating)
    VALUES (?, ?, ?, ?);
    """, (new_book_id, book_title, author_id, rating))

    conn.commit()
    conn.close()

    print("Book added successfully.")


def update_rating():
    book_title = input("Enter book title to update: ")
    new_rating = input("Enter new rating: ")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE Books
    SET Avg_Rating = ?
    WHERE Book = ?;
    """, (new_rating, book_title))

    conn.commit()
    conn.close()

    print("Book rating updated successfully.")


def delete_book():
    book_title = input("Enter book title to delete: ")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM Books
    WHERE Book = ?;
    """, (book_title,))

    conn.commit()
    conn.close()

    print("Book deleted successfully.")


def main():
    while True:
        print("\n--- Book Database Menu ---")
        print("1. View books")
        print("2. Search by author")
        print("3. Add book")
        print("4. Update book rating")
        print("5. Delete book")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            view_books()
        elif choice == "2":
            search_by_author()
        elif choice == "3":
            add_book()
        elif choice == "4":
            update_rating()
        elif choice == "5":
            delete_book()
        elif choice == "6":
            print("Goodbye.")
            break
        else:
            print("Invalid option. Please try again.")


main()