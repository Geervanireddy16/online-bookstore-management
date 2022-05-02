# function to get all books
def allBooks(db):
    booksData = db.books.find({"isdeleted":False})
    ans = []
    for book in booksData:
        ans.append(book)
    # booksData = list(booksData)
    # print(booksData
    return ans

# function to get all genre
def allGenre(db):
    genreData = db.books.distinct("genre", {"isdeleted":False})
    ans = []
    for genre in genreData:
        ans.append(str(genre))
    return ans