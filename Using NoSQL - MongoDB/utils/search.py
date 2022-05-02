def searchTitle(db,query):
    ans = []
    booksData = db.books.find({ "title": { "$regex": "(?i)"+str(query)} ,"isdeleted":False})
    for i in booksData:
        ans.append(i)
    return ans

def searchGenre(db,query):
    booksData = db.books.find({ "genre": { "$regex": "(?i)"+str(query)},"isdeleted":False })
    ans = []
    for book in booksData:
        ans.append(book)
    return ans

def searchAuthor(db,query):
    booksData = db.books.find({ "authorname": { "$regex": "(?i)"+str(query)},"isdeleted":False })
    ans = []
    for book in booksData:
        ans.append(book)
    return ans