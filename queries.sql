-- Query 1: Shows each book with its author name and average rating
SELECT 
    Books.Book,
    Author.AuthorName,
    Books.Avg_Rating
FROM Books
JOIN Author
ON Books.AuthorID = Author.AuthorID;


-- Query 2: Shows each book with its linked genre or genres
SELECT
    Books.Book,
    Genre.Genre
FROM Books
JOIN BookGenre
ON Books.BookID = BookGenre.BookID
JOIN Genre
ON BookGenre.GenreID = Genre.GenreID
ORDER BY Books.BookID;


-- Query 3: Filters books by the selected genre and sorts them by rating
SELECT
    Books.Book,
    Author.AuthorName,
    Genre.Genre,
    Books.Avg_Rating
FROM Books
JOIN Author
ON Books.AuthorID = Author.AuthorID
JOIN BookGenre
ON Books.BookID = BookGenre.BookID
JOIN Genre
ON BookGenre.GenreID = Genre.GenreID
WHERE Genre.Genre = 'Fantasy'
ORDER BY Books.Avg_Rating DESC;


-- Query 4: Searches for books by a selected author
SELECT
    Books.Book,
    Author.AuthorName,
    Books.Avg_Rating
FROM Books
JOIN Author
ON Books.AuthorID = Author.AuthorID
WHERE Author.AuthorName = 'Jane Austen'
ORDER BY Books.Avg_Rating DESC;