# function to get all books
def allBooks(mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName FROM Books as b INNER JOIN Authors as a ON b.authorID = a.authorID  ORDER BY bookID")
    booksData = cur.fetchall()
    booksData = list(booksData)
    mysql.connection.commit()
    cur.close()
    return booksData

# function to get all genre
def allGenre(mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT DISTINCT genre from Books")
    genreData = list(cur.fetchall())
    mysql.connection.commit()
    cur.close()
    return genreData