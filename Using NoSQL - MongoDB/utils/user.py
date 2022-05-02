def admin(db):
    adminData = db.users.find({"account":"admin"})
    # cur.execute("SELECT * from Admins")
    # adminData = list(cur.fetchall())
    return adminData

def customers(db):
    customerData = db.users.find({"account":"customer"})
    return customerData

def adminAccount(db,userID):
    Data = db.users.find_one({"username":userID})
    # cur.execute("SELECT * from Admins WHERE adminID = %s",(userID,))
    # Data = list(cur.fetchone())
    return Data

def customerAccount(db,userID):
    Data = db.users.find_one({"username":userID})
    return Data

# def contactUs(mysql,fname,lname,email,message,timestamp):
#     cur = mysql.connection.cursor()

#     try:
#         cur.execute("INSERT INTO ContactUs(firstName,lastName,emailID,message,timestamp) VALUES (%s,%s,%s,%s,%s)",(fname,lname,email,message,timestamp))
#         result = 1 # insert successful
#     except:
#         result = 0 # insert unsuccessful

#     mysql.connection.commit()
#     cur.close()
#     return result