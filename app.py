from flask import Flask, jsonify,request,render_template
from flask_mysqldb import MySQL
import MySQLdb.cursors,re

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

# app.config['MYSQL_HOST'] = '127.0.0.1'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'bookstore'

mysql = MySQL(app)
# home route function for testing purposes
@app.route("/")
def home():
    return render_template("home.html")
    return "HOME PAGE"

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
                return render_template("index.html")

            mysql.connection.commit()
            cur.close()
            return render_template("login.html")

        if account=="admin":
            print("-----------------Admin-----------------")
            cur = mysql.connection.cursor()
            cur.execute("SELECT * from Admins WHERE adminID = %s AND password = %s",(username,password))
            check = cur.fetchall()
            check = list(check)
            print(check)

            if not check:
                print("Fail")
                return render_template("login.html")
            else:
                print("Success")
                return render_template("adminindex.html")

            mysql.connection.commit()
            cur.close()
            return render_template("login.html")

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)

