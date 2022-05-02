# add book function
def addBook(mysql,bookID,title,genre,fname,lname,year,price,country,stock):
    cur = mysql.connection.cursor()
    try:
        # if publisher country is not present in Publishers table then add record
        cur.execute("SELECT publisherID from Publishers WHERE country = %s",(country,))
        publisherID = list(cur.fetchall())
        if not publisherID:
            cur.execute("INSERT INTO Publishers(country) VALUES (%s)",(country,))
            cur.execute("SELECT publisherID from Publishers WHERE country = %s",(country,))
            publisherID = list(cur.fetchall())

        # if author name is not present in Authors table then add record
        cur.execute("SELECT authorID from Authors WHERE firstName = %s AND lastName = %s",(fname,lname,))
        authorID = list(cur.fetchall())
        if not authorID:
            cur.execute("INSERT INTO Authors(firstName,lastName) VALUES (%s,%s)",(fname,lname,))
            cur.execute("SELECT authorID from Authors WHERE firstName = %s AND lastName = %s",(fname,lname,))
            authorID = list(cur.fetchall())

        # add book in Books table
        cur.execute("INSERT INTO Books(bookID,authorID,publisherID,title,genre,publicationYear,price) VALUES (%s,%s,%s,%s,%s,%s,%s)",(bookID,authorID,publisherID,title,genre,year,price))
        
        # add book stock in Inventory
        cur.execute("INSERT INTO Inventory (bookID,totalStock,soldStock) VALUES(%s,%s,%s)",(bookID,stock,0))

        result = 1 # book added successfully
    
    except:
        result = 0 # book failed to add
    
    mysql.connection.commit()
    cur.close()

    return result

# update book function
def updateBook(mysql,bookID,price1,price2,fname,lname,country):
    cur = mysql.connection.cursor()

    try:
        cur.execute("SELECT authorID from Authors WHERE firstName = %s AND lastName = %s",(fname,lname,))
        authorID = list(cur.fetchall())
        cur.execute("SELECT publisherID from Publishers WHERE country = %s",(country,))
        publisherID = list(cur.fetchall())
        cur.execute("UPDATE Books SET price = %s WHERE bookID = %s AND authorID = %s AND publisherID  = %s AND price = %s",(price2,bookID,authorID[0],publisherID[0],price1))
        result = 1 # book updated successfully
     
    except:
        result = 0 # book failed to update

    mysql.connection.commit()
    cur.close()

    return result

# delete book function
def deleteBook(mysql,bookID,fname,lname,country):
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT authorID from Authors WHERE firstName = %s AND lastName = %s",(fname,lname))
        authorID = list(cur.fetchone())
        cur.execute("SELECT count(authorID) from Books WHERE authorID = %s",(authorID))
        authorbooks = list(cur.fetchone())
        cur.execute("SELECT publisherID FROM Publishers WHERE country = %s",(country,))
        publisherID = list(cur.fetchone())
        cur.execute("SELECT count(authorID) FROM Books WHERE publisherID = %s",(publisherID,))
        publisherbooks = list(cur.fetchone())
        # delete from Inventory first and then from Books because of foreign key constraint
        cur.execute("DELETE FROM Inventory WHERE bookID = %s",(bookID,))
        cur.execute("DELETE FROM Books WHERE bookID = %s",(bookID,))

        # delete from authors table if books'author has not more than one book
        if authorbooks[0] == 1:
            cur.execute("DELETE FROM Authors WHERE authorID = %s",(authorID[0],))
        
         # delete from publishers table if books'publishers has not more than one book published
        if publisherbooks[0] == 1:
            cur.execute("DELETE FROM Publishers WHERE publisherID = %s",(publisherID[0],))
        
        result = 1 # book deleted successfully 
    
    except:
        result = 0 # book failed to delete

    mysql.connection.commit()
    cur.close()

    return result

# book stock function
def inventory(mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT b.bookID,b.title,i.totalStock,i.soldStock FROM Books as b,Inventory as i WHERE b.bookID=i.bookID")
    bookData = list(cur.fetchall())
    mysql.connection.commit()
    cur.close()
    return bookData

# book details function
def bookDetail(mysql,subject):
    cur = mysql.connection.cursor()
    cur.execute("SELECT b.bookID,b.title,b.genre,b.price,b.publicationYear,a.firstName,a.lastName,p.country FROM Books as b JOIN Authors as a ON b.authorID = a.authorID JOIN Publishers as p on b.publisherID = p.publisherID WHERE b.bookID = %s",(subject,))
    bookData = list(cur.fetchone())
    mysql.connection.commit()
    cur.close()
    return bookData

# calcuate total cost of books
def totalBookPrice(mysql,bookID,quantity):
    cur = mysql.connection.cursor()
    cur.execute("SELECT bookID,price,title from Books where bookID = %s",(bookID,))
    bookData = list(cur.fetchone())
    mysql.connection.commit()
    cur.close()
    return bookData
