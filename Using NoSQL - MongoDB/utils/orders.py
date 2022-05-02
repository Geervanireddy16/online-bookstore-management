import datetime

def orders(db,isbn,quantity,total,pay,userID):
    if pay == "1":
        timestamp = datetime.datetime.now()
        data = {
            "customer_username":userID,
            "quantity":int(quantity),
            "bookID":int(isbn),
            "total_price":int(total),
            "timestamp":timestamp
        }
        db.orders.insert_one(data)
        return 1
    return 0


# function to display all orders to admin portal
def allorders(db,userID):
    ans = []
    data = db.orders.find({})
    for i in data:
        ans.append(i)
    return ans
    return Data

# function to display customers orders
def myorder(db,userID):
    ans = []
    data = db.orders.find({"customer_username":userID})
    for i in data:
        ans.append(i)
    return ans