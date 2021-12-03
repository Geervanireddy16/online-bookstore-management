def searchTitle(mysql,query):
    cur = mysql.connection.cursor()
    cur.execute("SELECT b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName FROM Books as b,Authors as a WHERE title LIKE %s AND b.authorID = a.authorID",({'%' + query + '%'}))
    booksData = list(cur.fetchall())
    mysql.connection.commit()
    cur.close()
    return booksData

def searchGenre(mysql,query):
    cur = mysql.connection.cursor()
    cur.execute("SELECT b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName FROM Books as b, Authors as a WHERE b.genre LIKE %s AND b.authorID = a.authorID",({'%' + query + '%'}))
    booksData = list(cur.fetchall())
    mysql.connection.commit()
    cur.close()
    return booksData

def searchAuthor(mysql,query):
    cur = mysql.connection.cursor()
    cur.execute("SELECT b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName FROM Books as b,Authors as a WHERE a.firstName LIKE %s AND b.authorID = a.authorID",({'%' + query + '%'}))
    list1Data = list(cur.fetchall()) # search query matching with the first name of the author
    cur.execute("SELECT b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName FROM Books as b,Authors as a WHERE a.lastName LIKE %s AND b.authorID = a.authorID",({'%' + query + '%'}))
    list2Data = list(cur.fetchall()) # search query matching with the last name of the author
    booksData = list(set(list1Data) | set(list2Data))   # without repition
    mysql.connection.commit()
    cur.close()
    return booksData