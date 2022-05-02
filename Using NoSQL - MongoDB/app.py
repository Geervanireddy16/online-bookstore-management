from flask import Flask,jsonify,request,render_template,redirect,url_for,session
import re,datetime,os
from os import getenv
from dotenv import load_dotenv
import sys
from pymongo import MongoClient
from flask_pymongo import PyMongo
import pprint
from bson.objectid import ObjectId

load_dotenv()
from utils.loginregister import *
from utils.home import *
from utils.book import *
from utils.orders import *
from utils.search import *
from utils.user import *


app = Flask(__name__)

app.secret_key = 'geervani'
db_link = getenv('MONGO',None)
db_name = getenv('DB_NAME',None)

client = MongoClient(db_link)
db = client.get_database(db_name) 

# home page route
@app.route("/")
def homeRoute():
    booksData = allBooks(db)
    genreData = allGenre(db)
    return render_template("home.html",booksData=booksData,genreData=genreData)

# home page for customers
@app.route("/customerindex",methods=["POST","GET"])
def customerindexRoute():
    booksData = allBooks(db)
    genreData = allGenre(db)
    return render_template("customerindex.html",booksData=booksData,genreData=genreData)

# home page for admins
@app.route("/adminindex",methods=["POST","GET"])
def adminindexRoute():
    booksData = allBooks(db)
    genreData = allGenre(db)
    return render_template("adminindex.html",booksData=booksData,genreData=genreData)

# Customer Registration route
@app.route("/register",methods=["POST","GET"])
def registerRoute():
    if request.method == "POST":
        username = request.form.get("username")
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        email = str(request.form.get("email"))
        password = request.form.get("password")
        phone = request.form.get("phone")
        country = request.form.get("country")
        state = request.form.get("state")
        pincode = request.form.get("pincode")
        address = str(request.form.get("address"))

        response = register(db,username,fname,lname,email,password,phone,country,state,pincode,address)
        
        if response == 1: # regsitration is successful
            return render_template("login.html",response=response)
        else: # registration failed
            return render_template("register.html",response=response)

    return render_template("register.html")

# login for customers and admins route
@app.route("/login",methods=["POST","GET"])
def loginRoute():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        account = request.form.get("account")

        if account=="customer":
            response = customerLogin(db,username,password,account)
            if response == 1: # login success
                session["userID"] = username # creating a session of the username
                session["accountType"] = account # creating a session of the account type
                return redirect(url_for("customerindexRoute"))
                # return("success")
            else: # Login failed
                return render_template("login.html",response = response)

        if account=="admin":
            response = adminLogin(db,username,password,account)
            if response == 1: # login success
                session["userID"] = username # creating a session of the username
                session["accountType"] = account # creating a session of the account type
                return redirect(url_for("adminindexRoute"))
                # return("success")
            else: # login failed
                return render_template("login.html",response=response)

    return render_template("login.html")

# search books in admin portal
@app.route("/search",methods=["POST","GET"])
def searchRoute():
    if request.method == "POST":
        search = str(request.form.get("search"))
        query = str(request.form.get("query"))

        if search == "title": # search by title
            booksData = searchTitle(db,query)
            return render_template("search.html",booksData=booksData,search=search)
        
        if search == "genre": # search by genre
            booksData = searchGenre(db,query)
            return render_template("search.html",booksData=booksData,search=search)
        
        if search == "author": # search by author
            booksData = searchGenre(db,query)
            return render_template("search.html",booksData=booksData,search=search)
            # booksData = searchAuthor(db,query)
            # return render_template("search.html",booksData=booksData,search=search)

        return render_template("search.html")
    
    return render_template("search.html")

# # search books in admin portal
@app.route("/customersearch",methods=["POST","GET"])
def customersearchRoute():
    if request.method == "POST":
        search = str(request.form.get("search"))
        query = str(request.form.get("query"))

        if search == "title": # search by title
            booksData = searchTitle(db,query)
            return render_template("customersearch.html",booksData=booksData,search=search)
        
        if search == "genre": # search by genre
            booksData = searchGenre(db,query)
            return render_template("customersearch.html",booksData=booksData,search=search)
        
        if search == "author": # search by author
            booksData = searchAuthor(db,query)
            return render_template("customersearch.html",booksData=booksData,search=search)

        return render_template("customersearch.html")
    
    return render_template("customersearch.html")

# # Add/Delete/Update Book Route for Admin
@app.route("/books",methods=["POST","GET"])
def booksRoute():
        booksData = allBooks(db)
        genreData = allGenre(db)
        return render_template("books.html",booksData=booksData,genreData=genreData)


# # Add Book Route
@app.route("/addBook",methods=["POST","GET"])
def addBookRoute():
    if request.method == "POST":
        bookID = str(request.form.get("bookID"))
        title = str(request.form.get("title"))
        genre = str(request.form.get("genre"))
        fname = str(request.form.get("fname"))
        lname = str(request.form.get("lname"))
        year = str(request.form.get("year"))
        price = request.form.get("price")
        country = str(request.form.get("country"))
        stock = str(request.form.get("stock"))

        response = addBook(db,bookID,title,genre,fname,lname,year,price,country,stock)
        if response == 1: # Book Added Successfully
            booksData = allBooks(db)
            genreData = allGenre(db)
            # return ("success")
            return render_template("books.html",booksData=booksData,genreData=genreData,response=response)
        else: # book failed to add
            booksData = allBooks(db)
            genreData = allGenre(db)
            # return ("fail")
            return render_template("books.html",booksData=booksData,genreData=genreData,response=response)

        return "home"
    # return redirect(url_for("booksRoute"))

# # Update Book Route
@app.route("/updateBook",methods=["POST","GET"])
def updateBookRoute():
    if request.method == "POST":
        bookID = int(request.form.get("bookID"))
        price1 = int(request.form.get("price1"))
        price2 = int(request.form.get("price2"))
        fname = str(request.form.get("fname"))
        lname = str(request.form.get("lname"))
        country = str(request.form.get("country"))

        response = updateBook(db,bookID,price1,price2,fname,lname,country)
        if response == 1: # book updated successfully
            booksData = allBooks(db)
            genreData = allGenre(db)
            return render_template("books.html",booksData=booksData,genreData=genreData,response=response)

        else: # book failed to update
            booksData = allBooks(db)
            genreData = allGenre(db)
            return render_template("books.html",booksData=booksData,genreData=genreData,response=response)

    return redirect(url_for("booksRoute"))

# # delete book Route
@app.route("/deleteBook",methods=["POST","GET"])
def deleteBookRoute():
    if request.method == "POST":
        bookID = str(request.form.get("bookID"))
        fname = str(request.form.get("fname"))
        lname = str(request.form.get("lname"))
        country = str(request.form.get("country"))

        response = deleteBook(db,bookID,fname,lname,country)
        if response == 1: # book deleted successfully
            booksData = allBooks(db)
            genreData = allGenre(db)
            return render_template("books.html",booksData=booksData,genreData=genreData,response=response)

        else: # book failed to delete
            booksData = allBooks(db)
            genreData = allGenre(db)
            return render_template("books.html",booksData=booksData,genreData=genreData,response=response)

    return redirect(url_for("booksRoute"))

# display book details route for customers
@app.route("/bookdetail<subject>",methods=["POST","GET"])
def bookDetailsRoute(subject):
    bookData = bookDetail(db,subject)
    # print(subject)
    if bookData == "error":
        return "error"

    return render_template("bookdetail.html",bookData=bookData)

# display book details route for admin
@app.route("/bookDetailsAdmin<subject>",methods=["POST","GET"])
def bookDetailsAdminRoute(subject):
    print("hi")
    print(subject)
    bookData = bookDetail(db,subject)
    return render_template("bookdetail2.html",bookData=bookData)

# buy book route
@app.route("/buyBook<bookID>",methods=["POST","GET"])
def buyBookRoute(bookID):
    if request.method =="POST":
        quantity = str(request.form.get("quantity"))
        # print("hi-bybook")
        # print(bookID)
        bookData = bookDetail(db,bookID)
        totalPrice = int(int(bookData['price'])*int(quantity))
        return render_template("payment.html",bookData=bookData,quantity=quantity,totalPrice=totalPrice)
        
    return "USE POST METHOD ONLY"
    
# pay order route
@app.route("/pay<isbn>/<quantity>/<total>",methods=["POST","GET"])
def payRoute(isbn,quantity,total):
    if request.method =="POST":
        pay = str(request.form.get("pay"))
        response = orders(db,isbn,quantity,total,pay,session["userID"])
        return redirect(url_for('orderconfirmationRoute',response = response))
        # return render_template("orderconfirmation.html",response=response)

    return "USE POST METHOD ONLY"

# # order confirmation route
@app.route("/orderconfirmation<response>",methods=["POST","GET"])
def orderconfirmationRoute(response):
    return render_template("orderconfirmation.html",response=response)

# inventory route
@app.route("/inventory",methods=["POST","GET"])
def inventoryRoute():
    bookData = inventory(db)
    for i in bookData:
        print(i)
    return render_template("inventory.html",bookData=bookData)

# # display users route
@app.route("/users",methods=["POST","GET"])
def usersRoute():
    adminData = admin(db)
    customerData = customers(db)
    return render_template("users.html",adminData=adminData,customerData=customerData)

# display  orders in customers and admins account account
@app.route("/myorders",methods=["POST","GET"])
def ordersRoute():
    userID = session["userID"]
    accountType = session["accountType"]

    if session["accountType"] == None or session["userID"]== None:
        return "ERROR"

    if session["accountType"]=="admin":
        Data = allorders(db,userID)
        return render_template("myorders.html",Data=Data,accountType=accountType)

    if session["accountType"]=="customer":
        Data = myorder(db,userID)
        return render_template("myorders.html",Data=Data,accountType=accountType)
    
#     return "ERROR"

# # display logged in users account
@app.route("/myaccount",methods=["POST","GET"])
def myAccountRoute():
    userID = session["userID"]
    accountType = session["accountType"]

    if session["accountType"] == None or session["userID"]== None:
        return "ERROR"

    if session["accountType"]=="admin":
        Data = adminAccount(db,userID)
        return render_template("myaccount.html",Data=Data,accountType=accountType)

    if session["accountType"]=="customer":
        Data = customerAccount(db,userID)
        return render_template("myaccount.html",Data=Data,accountType=accountType)
    
    return "ERROR"



# logout route
@app.route("/logout",methods = ["GET","POST"])
def logoutRoute():
    session.pop("userID",None) # removing username from session variable
    session.pop("accountType",None) # removing account from session variable
    booksData = allBooks(db)
    genreData = allGenre(db)
    return render_template("home.html",booksData=booksData,genreData=genreData)



if __name__ == "__main__":
    app.run(debug=True)
