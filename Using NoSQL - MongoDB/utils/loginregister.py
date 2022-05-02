from pymongo import MongoClient
import pprint
from bson.objectid import ObjectId

# function to register customer
def register(db,username,fname,lname,email,password,phone,country,state,pincode,address):        
    # cur = mysql.connection.cursor()
    users = db.users
    try:
        data = {
            "username":username,
            "account":"customer",
            "fname":fname,
            "lname":lname,
            "email":email,
            "password":password,
            "phone":int(phone),
            "country":country,
            "state":state,
            "pincode":int(pincode),
            "address":address
        }
        db.users.insert_one(data)
        result = 1 # registration successful
    except:
        result =  0 # registration failed
    
    return result

# function for admin login
def adminLogin(db,username,password,account):
    check = db.users.find_one({"username":username,"password":password,"account":account})
    if not check:
        result = 0 # login failed
    else:
        result = 1 # login success
    
    return result

# function for customer login
def customerLogin(db,username,password,account):
    check = db.users.find_one({"username":username,"password":password,"account":account})

    if not check:
        result = 0 # login failed
    else:
        result = 1 # login success

    return result
