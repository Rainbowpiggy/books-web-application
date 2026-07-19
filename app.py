from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

DATABASE = "database/books.db"


def get_books(search_text="", selected_genre=""):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
    SELECT 
        Books.BookID,
        Books.Book,
        Author.AuthorName,
        REPLACE(GROUP_CONCAT(DISTINCT Genre.Genre), ',', ', ') AS Genres,
        Books.Avg_Rating
    FROM Books
    JOIN Author
        ON Books.AuthorID = Author.AuthorID
    JOIN BookGenre
        ON Books.BookID = BookGenre.BookID
    JOIN Genre
        ON BookGenre.GenreID = Genre.GenreID
    WHERE 1 = 1
    """

    values = []

    if search_text:
        query += """
        AND (Books.Book LIKE ? OR Author.AuthorName LIKE ?)
        """
        values.append("%" + search_text + "%")
        values.append("%" + search_text + "%")

    if selected_genre:
        query += """
        AND Books.BookID IN (
            SELECT BookGenre.BookID
            FROM BookGenre
            JOIN Genre
                ON BookGenre.GenreID = Genre.GenreID
            WHERE Genre.Genre = ?
        )
        """
        values.append(selected_genre)

    query += """
    GROUP BY Books.BookID, Books.Book, Author.AuthorName, Books.Avg_Rating
    ORDER BY Books.Avg_Rating DESC
    LIMIT 8;
    """

    cursor.execute(query, values)
    books = cursor.fetchall()

    conn.close()
    return books


def get_genres():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
    SELECT Genre
    FROM Genre
    ORDER BY Genre;
    """)

    genres = cursor.fetchall()

    conn.close()
    return genres


@app.route("/")
def home():
    search_text = request.args.get("search", "")
    selected_genre = request.args.get("genre", "")

    books = get_books(search_text, selected_genre)
    genres = get_genres()

    return render_template(
        "index.html",
        books=books,
        genres=genres,
        search_text=search_text,
        selected_genre=selected_genre
    )


if __name__ == "__main__":
    app.run(debug=True)