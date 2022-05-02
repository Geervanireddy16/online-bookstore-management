
# add book function
def addBook(db,bookID,title,genre,fname,lname,year,price,country,stock):

    try:
        data = {
            "bookID":int(bookID),
            "title":title,
            "genre": genre,
            "authorname":str(fname+" "+lname),
            "price":int(price),
            "publicationyear":int(year),
            "publicationcountry":country,
            "soldStock":int(0),
            "totalStock":int(stock),
            "isdeleted":False
        }
        db.books.insert_one(data)  # add book in Books collection
        result = 1 # book added successfully
    
    except:
        result = 0 # book failed to add

    return result

# update book function
def updateBook(db,bookID,price1,price2,fname,lname,country):
    try:
        db.books.update_one({"bookID":int(bookID),"price":int(price1),"isdeleted":False},{"$set": {"price": int(price2)}})
        result = 1 # book updated successfully
    except:
        result = 0 # book failed to update

    return result

# delete book function
def deleteBook(db,bookID,fname,lname,country):
    try:
        db.books.update_one({"bookID":int(bookID),"authorname":str(fname+" "+lname),"publicationcountry":country,"isdeleted":False},{"$set": {"isdeleted": True}})
        result = 1 # book deleted successfully 
    
    except:
        result = 0 # book failed to delete

    return result

# book stock function
def inventory(db):
    bookData = db.books.find({"isdeleted":False})
    ans = []
    for book in bookData:
        ans.append(book)
        # ans.append(book["_id"],book["bookID"],book["totalStock"],book("soldStock"),book["title"])
    return ans

# book details function
def bookDetail(db,subject):
    try:
        booksData = db.books.find_one({"bookID":int(subject)})
        return booksData
    except:
        return "error"


