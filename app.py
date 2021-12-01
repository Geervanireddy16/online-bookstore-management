from flask import Flask, jsonify,request,render_template,redirect,url_for,session
from flask_mysqldb import MySQL
import MySQLdb.cursors,re

import datetime
import os
from os import getenv
from dotenv import load_dotenv

load_dotenv()
mysql_host = getenv('MYSQL_HOST',None)
mysql_user = getenv('MYSQL_USER',None)
mysql_password = getenv('MYSQL_PASSWORD',None)
mysql_db = getenv('MYSQL_DB',None)


app = Flask(__name__)

app.config['MYSQL_HOST'] = mysql_host
app.config['MYSQL_USER'] = mysql_user
app.config['MYSQL_PASSWORD'] = mysql_password
app.config['MYSQL_DB'] = mysql_db

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # all the session data is encrypted in the server so we need a secret key to encrypt and decrypt the data

# app.config['MYSQL_HOST'] = '127.0.0.1'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'bookstore'

mysql = MySQL(app)
# home route function for testing purposes
@app.route("/")
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName  FROM Books as b INNER JOIN Authors as a ON b.authorID = a.authorID  ORDER BY bookID")
    booksData = cur.fetchall()
    booksData = list(booksData)
    cur.execute("SELECT DISTINCT genre from Books")
    genreData = list(cur.fetchall())
    mysql.connection.commit()
    cur.close()
    return render_template("home.html",booksData=booksData,genreData=genreData)

@app.route("/register",methods=["POST","GET"])
def register():
    if request.method == "POST":
        username = str(request.form.get("username"))
        fname = str(request.form.get("fname"))
        lname = str(request.form.get("lname"))
        email = str(request.form.get("email"))
        password = str(request.form.get("password"))
        phone = str(request.form.get("phone"))
        country = str(request.form.get("country"))
        state = str(request.form.get("state"))
        pincode = str(request.form.get("pincode"))
        address = str(request.form.get("address"))
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Customers(customerID,firstName,lastName,address,pincode,country,phone,state,emailID,password) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(username,fname,lname,address,pincode,country,phone,state,email,password))
        mysql.connection.commit()
        cur.close()
        print("Registered Successfully")
        return render_template("login.html")

    return render_template("register.html")
    # return redirect("/login")

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        account = request.form.get("account")
        print(username)
        print(password)
        print(account)
        session["userID"] = username # creating a session of the username
        session["accountType"] = account # creating a session of the account type

        if account=="customer":
            print("-----------------Customer-----------------")
            cur = mysql.connection.cursor()
            cur.execute("SELECT * from Customers WHERE customerID = %s AND password = %s",(username,password))
            check = cur.fetchall()
            check = list(check)
            print(check)

            if not check:
                print("Fail")
                return render_template("login.html")
            else:
                print("Success")
                return redirect(url_for("customerindex"))
                # cur = mysql.connection.cursor()
                # cur.execute("SELECT b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName  FROM Books as b INNER JOIN Authors as a ON b.authorID = a.authorID  ORDER BY bookID")
                # # cur.execute("SELECT * from Books")
                # booksData = cur.fetchall()
                # booksData = list(booksData)
                # cur.execute("SELECT DISTINCT genre from Books")
                # genreData = list(cur.fetchall())
                # # print(genreData)
                # # print(booksData)
                # mysql.connection.commit()
                # cur.close()
                # return render_template("adminindex.html",booksData=booksData,genreData=genreData)

            mysql.connection.commit()
            cur.close()
            return render_template("login.html")

        if account=="admin":
            print("-----------------Admin-----------------")
            # session["userID"] = username # creating a session of the username
            # session["accountType"] = account # creating a session of the account type
            print("LOGIN")
            print(session["userID"])
            print(session["accountType"])

            cur = mysql.connection.cursor()
            cur.execute("SELECT * from Admins WHERE adminID = %s AND password = %s",(username,password))
            check = cur.fetchall()
            check = list(check)
            print(check)
            mysql.connection.commit()
            cur.close()

            if not check:
                print("Fail")
                return render_template("login.html")
            else:
                print("Success")
                return redirect(url_for("adminindex"))
                # cur = mysql.connection.cursor()
                # cur.execute("SELECT b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName  FROM Books as b INNER JOIN Authors as a ON b.authorID = a.authorID  ORDER BY bookID")
                # # cur.execute("SELECT * from Books")
                # booksData = cur.fetchall()
                # booksData = list(booksData)
                # cur.execute("SELECT DISTINCT genre from Books")
                # genreData = list(cur.fetchall())
                # # print(genreData)
                # # print(booksData)
                # mysql.connection.commit()
                # cur.close()
                # return render_template("adminindex.html",booksData=booksData,genreData=genreData)

            return render_template("login.html")

    return render_template("login.html")

@app.route("/adminindex",methods=["POST","GET"])
def adminindex():
        cur = mysql.connection.cursor()
        cur.execute("SELECT b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName  FROM Books as b INNER JOIN Authors as a ON b.authorID = a.authorID  ORDER BY bookID")
        # cur.execute("SELECT * from Books")
        booksData = cur.fetchall()
        booksData = list(booksData)
        cur.execute("SELECT DISTINCT genre from Books")
        genreData = list(cur.fetchall())
        # print(genreData)
        # print(booksData)
        mysql.connection.commit()
        cur.close()
        return render_template("adminindex.html",booksData=booksData,genreData=genreData)

@app.route("/customerindex",methods=["POST","GET"])
def customerindex():
        cur = mysql.connection.cursor()
        cur.execute("SELECT b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName  FROM Books as b INNER JOIN Authors as a ON b.authorID = a.authorID  ORDER BY bookID")
        # cur.execute("SELECT * from Books")
        booksData = cur.fetchall()
        booksData = list(booksData)
        cur.execute("SELECT DISTINCT genre from Books")
        genreData = list(cur.fetchall())
        # print(genreData)
        # print(booksData)
        mysql.connection.commit()
        cur.close()
        return render_template("customerindex.html",booksData=booksData,genreData=genreData)

@app.route("/search",methods=["POST","GET"])
def search():
    if request.method == "POST":
        search = str(request.form.get("search"))
        query = str(request.form.get("query"))


        if search == "title":
            cur = mysql.connection.cursor()
            cur.execute("SELECT b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName FROM Books as b,Authors as a WHERE title LIKE %s AND b.authorID = a.authorID",({'%' + query + '%'}))
            booksData = list(cur.fetchall())
            mysql.connection.commit()
            cur.close()
            return render_template("search.html",booksData=booksData,search=search)
        
        if search == "genre":
            cur = mysql.connection.cursor()
            cur.execute("SELECT b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName FROM Books as b, Authors as a WHERE b.genre = %s AND b.authorID = a.authorID",(query,))
            booksData = list(cur.fetchall())
            mysql.connection.commit()
            cur.close()
            return render_template("search.html",booksData=booksData,search=search)
        
        if search == "author":
            cur = mysql.connection.cursor()
            cur.execute("SELECT b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName FROM Books as b,Authors as a WHERE a.firstName LIKE %s AND b.authorID = a.authorID",({'%' + query + '%'}))
            list1Data = list(cur.fetchall())
            cur.execute("SELECT b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName FROM Books as b,Authors as a WHERE a.lastName LIKE %s AND b.authorID = a.authorID",({'%' + query + '%'}))
            list2Data = list(cur.fetchall())
            booksData = list(set(list1Data) | set(list2Data))   # without repition
            mysql.connection.commit()
            cur.close()
            return render_template("search.html",booksData=booksData,search=search)

        return render_template("search.html")
    
    return render_template("search.html")


@app.route("/customersearch",methods=["POST","GET"])
def customersearch():
    if request.method == "POST":
        search = str(request.form.get("search"))
        query = str(request.form.get("query"))

        if search == "title":
            cur = mysql.connection.cursor()
            cur.execute("SELECT b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName FROM Books as b,Authors as a WHERE title LIKE %s AND b.authorID = a.authorID",({'%' + query + '%'}))
            booksData = list(cur.fetchall())
            mysql.connection.commit()
            cur.close()
            return render_template("customersearch.html",booksData=booksData,search=search)
        
        if search == "genre":
            cur = mysql.connection.cursor()
            cur.execute("SELECT b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName FROM Books as b, Authors as a WHERE b.genre = %s AND b.authorID = a.authorID",(query,))
            booksData = list(cur.fetchall())
            mysql.connection.commit()
            cur.close()
            return render_template("customersearch.html",booksData=booksData,search=search)
        
        if search == "author":
            cur = mysql.connection.cursor()
            cur.execute("SELECT b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName FROM Books as b,Authors as a WHERE a.firstName LIKE %s AND b.authorID = a.authorID",({'%' + query + '%'}))
            list1Data = list(cur.fetchall())
            cur.execute("SELECT b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName FROM Books as b,Authors as a WHERE a.lastName LIKE %s AND b.authorID = a.authorID",({'%' + query + '%'}))
            list2Data = list(cur.fetchall())
            booksData = list(set(list1Data) | set(list2Data))   # without repition
            mysql.connection.commit()
            cur.close()
            return render_template("customersearch.html",booksData=booksData,search=search)

        return render_template("customersearch.html")
    
    return render_template("customersearch.html")


@app.route("/books",methods=["POST","GET"])
def books():
    # if request.method == "POST":
        cur = mysql.connection.cursor()
        # cur.execute("SELECT * from Books as b,Authors as a where b.authorID = a.authorID")
        cur.execute("SELECT b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName  FROM Books as b INNER JOIN Authors as a ON b.authorID = a.authorID  ORDER BY bookID")
        booksData = cur.fetchall()
        booksData = list(booksData)
        cur.execute("SELECT DISTINCT genre from Books")
        genreData = list(cur.fetchall())
        print("HIIIIIIIIIIIIIIIIIIIIIIIIII")
        print(genreData)
        print(booksData)
        mysql.connection.commit()
        cur.close()
        return render_template("books.html",booksData=booksData,genreData=genreData)

    # else:
    #     print("FAILL")
        
    # return render_template("books.html")
    # return "HIIII"

@app.route("/addBook",methods=["POST","GET"])
def addBook():
    if request.method == "POST":

        # print("inn")
        bookID = str(request.form.get("bookID"))
        title = str(request.form.get("title"))
        genre = str(request.form.get("genre"))
        fname = str(request.form.get("fname"))
        lname = str(request.form.get("lname"))
        year = str(request.form.get("year"))
        price = str(request.form.get("price"))
        country = str(request.form.get("country"))

        cur = mysql.connection.cursor()
        cur.execute("SELECT publisherID from Publishers WHERE country = %s",(country,))
        publisherID = list(cur.fetchall())
        print(publisherID)
        if not publisherID:
            print("PublisherID not present")
            # cur.execute("INSERT INTO Customers(customerd) VALUES (%s,%s,)",(username,email,password))
            cur.execute("INSERT INTO Publishers(country) VALUES (%s)",(country,))
            cur.execute("SELECT publisherID from Publishers WHERE country = %s",(country,))
            publisherID = list(cur.fetchall())
            print(publisherID)


        cur.execute("SELECT authorID from Authors WHERE firstName = %s AND lastName = %s",(fname,lname,))
        authorID = list(cur.fetchall())
        print(authorID)
        if not authorID:
            print("authorID not present")
            cur.execute("INSERT INTO Authors(firstName,lastName) VALUES (%s,%s)",(fname,lname,))
            cur.execute("SELECT authorID from Authors WHERE firstName = %s AND lastName = %s",(fname,lname,))
            authorID = list(cur.fetchall())
            print(authorID)

        cur.execute("INSERT INTO Books(bookID,authorID,publisherID,title,genre,publicationYear,price) VALUES (%s,%s,%s,%s,%s,%s,%s)",(bookID,authorID,publisherID,title,genre,year,price))
        print("Book Added Successfully")
        
        mysql.connection.commit()
        cur.close()


        return redirect(url_for("books"))
    # return render_template("product_detail.html")
    return "HOME PAGE"

@app.route("/updateBook",methods=["POST","GET"])
def updateBook():
    if request.method == "POST":
        bookID = str(request.form.get("bookID"))
        price1 = str(request.form.get("price1"))
        price2 = str(request.form.get("price2"))
        # genre = str(request.form.get("genre"))
        fname = str(request.form.get("fname"))
        lname = str(request.form.get("lname"))
        country = str(request.form.get("country"))

        cur = mysql.connection.cursor()
        cur.execute("SELECT authorID from Authors WHERE firstName = %s AND lastName = %s",(fname,lname,))
        authorID = list(cur.fetchall())
        cur.execute("SELECT publisherID from Publishers WHERE country = %s",(country,))
        publisherID = list(cur.fetchall())
        # cur.execute("INSERT INTO Books(authorID,publisherID,title,genre,publicationYear,price) VALUES (%s,%s,%s,%s,%s,%s)",(authorID,publisherID,title,genre,year,price))
        cur.execute("UPDATE Books SET price = %s WHERE bookID = %s AND authorID = %s AND publisherID  = %s AND price = %s",(price2,bookID,authorID[0],publisherID[0],price1))
        print("Book Price update Successfully")
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("books"))
    # return render_template("product_detail.html")
    return "HOME PAGE"


@app.route("/deleteBook",methods=["POST","GET"])
def deleteBook():
    if request.method == "POST":
        bookID = str(request.form.get("bookID"))
        # title = str(request.form.get("title"))
        # genre = str(request.form.get("genre"))
        # price = str(request.form.get("price"))
        fname = str(request.form.get("fname"))
        lname = str(request.form.get("lname"))
        country = str(request.form.get("country"))

        cur = mysql.connection.cursor()
        cur.execute("SELECT authorID from Authors WHERE firstName = %s AND lastName = %s",(fname,lname))
        authorID = cur.fetchone()
        cur.execute("SELECT count(authorID) from Books WHERE authorID = %s",(authorID))
        authorbooks = cur.fetchone()
        cur.execute("SELECT publisherID FROM Publishers WHERE country = %s",(country,))
        publisherID = cur.fetchone()
        cur.execute("SELECT count(authorID) FROM Books WHERE publisherID = %s",(publisherID,))
        publisherbooks = cur.fetchone()
        
        cur.execute("DELETE FROM Books WHERE bookID = %s",(bookID,))
        
        if authorbooks[0] == 1:
            cur.execute("DELETE FROM Authors WHERE authorID = %s",(authorID[0],))
        if publisherbooks[0] == 1:
            cur.execute("DELETE FROM Publishers WHERE publisherID = %s",(publisherID[0],))
        
        print("Book deleted Successfully")
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("books"))
    # return render_template("product_detail.html")
    return "HOME PAGE"


@app.route("/users",methods=["POST","GET"])
def users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from Admins")
    adminData = list(cur.fetchall())
    cur.execute("SELECT * from Customers")
    customerData = list(cur.fetchall())
    mysql.connection.commit()
    cur.close()
    return render_template("users.html",adminData=adminData,customerData=customerData)

@app.route("/myaccount",methods=["POST","GET"])
def myAccount():
    
    if session["accountType"]=="admin":
        cur = mysql.connection.cursor()
        userID = session["userID"]
        accountType = session["accountType"]
        print(userID)
        cur.execute("SELECT * from Admins WHERE adminID = %s",(userID,))
        Data = list(cur.fetchone())
        print(Data)
        return render_template("myaccount.html",Data=Data,accountType=accountType)
        # return "Hi"
        mysql.connection.commit()
        cur.close()
        # return render_template("myaccount.html",Data=Data)

    if session["accountType"]=="customer":
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from Customers WHERE customerID = %s",(session["userID"],))
        customerData = list(cur.fetchone())
        mysql.connection.commit()
        cur.close()
        account = session["accountType"]
        return render_template("myaccount.html",Data=customerData,accountType=account)
    return "ERROR"

@app.route("/contactUs",methods=["POST","GET"])
def contactUs():
    if request.method == "POST":
        fname = str(request.form.get("fname"))
        lname = str(request.form.get("lname"))
        email = str(request.form.get("email"))
        message = str(request.form.get("message"))
        timestamp = datetime.datetime.now()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO ContactUs(firstName,lastName,emailID,message,timestamp) VALUES (%s,%s,%s,%s,%s)",(fname,lname,email,message,timestamp))
        mysql.connection.commit()
        cur.close()
        return "Message Submitted"

    return "HOME PAGE"
    # return redirect("/login")

@app.route("/logout",methods = ["GET","POST"])
def logout():
    session.pop("userID",None) # removing username from session variable
    session.pop("accountType",None) # removing account from session variable
    print("---------------Logout----------------------")

    cur = mysql.connection.cursor()
    cur.execute("SELECT b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName  FROM Books as b INNER JOIN Authors as a ON b.authorID = a.authorID  ORDER BY bookID")
    booksData = cur.fetchall()
    booksData = list(booksData)
    cur.execute("SELECT DISTINCT genre from Books")
    genreData = list(cur.fetchall())
    mysql.connection.commit()
    cur.close()
    return render_template("home.html",booksData=booksData,genreData=genreData)

@app.route("/bookdetail<subject>",methods=["POST","GET"])
def bookDetails(subject):
    cur = mysql.connection.cursor()
    cur.execute("SELECT b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName  FROM Books as b,Authors as a WHERE b.bookID = %s AND b.authorID = a.authorID",(subject,))
    bookData = list(cur.fetchone())
    print(bookData)
    # booksData = list(booksData)
    return render_template("bookdetail.html",bookData=bookData)
    mysql.connection.commit()
    cur.close()

@app.route("/buyBook",methods=["POST","GET"])
def buyBook(subject):
    return "HII"

@app.route("/*")
def invalid():
    return "Invalid page"


if __name__ == "__main__":
    app.run(debug=True)

