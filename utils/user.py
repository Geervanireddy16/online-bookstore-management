def admin(mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from Admins")
    adminData = list(cur.fetchall())
    mysql.connection.commit()
    cur.close()
    return adminData

def customers(mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from Customers")
    customerData = list(cur.fetchall())
    mysql.connection.commit()
    cur.close()
    return customerData

def adminAccount(mysql,userID):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from Admins WHERE adminID = %s",(userID,))
    Data = list(cur.fetchone())
    mysql.connection.commit()
    cur.close()
    return Data

def customerAccount(mysql,userID):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from Customers WHERE customerID = %s",(userID,))
    customerData = list(cur.fetchone())
    mysql.connection.commit()
    cur.close()
    return customerData

def contactUs(mysql,fname,lname,email,message,timestamp):
    cur = mysql.connection.cursor()

    try:
        cur.execute("INSERT INTO ContactUs(firstName,lastName,emailID,message,timestamp) VALUES (%s,%s,%s,%s,%s)",(fname,lname,email,message,timestamp))
        result = 1 # insert successful
    except:
        result = 0 # insert unsuccessful

    mysql.connection.commit()
    cur.close()
    return result