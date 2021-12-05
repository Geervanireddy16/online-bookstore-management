import datetime

def orders(mysql,isbn,quantity,total,pay,userID):
    cur = mysql.connection.cursor()
    timestamp = datetime.datetime.now()
    commitStatus = 0

    try:
        mysql.connection.autocommit = False       
        cur.execute("INSERT into Orders(customerID,bookID,quantity,total,timestamp) values(%s,%s,%s,%s,%s)",(userID,isbn,quantity,total,timestamp))
        cur.execute("UPDATE Inventory set soldStock = soldStock + %s where bookID = %s",(quantity,isbn))
        cur.execute("UPDATE Inventory set totalStock = totalStock - %s where bookID = %s",(quantity,isbn))
        print('Transaction committed')
        
        try:
            mysql.connection.autocommit = False
            cur.execute("INSERT into Payment(customerID,paymentInfo) values (%s,%s)",(userID,pay)) # throws error if user enters incorrect payment information
            print('Payment Added')
            commitStatus = 1 # payment successful

        except:
            print("Transaction rolled back")
            mysql.connection.rollback()
        
    except:
        print("Transaction rolled back")
        mysql.connection.rollback()
    
    mysql.connection.commit()
    cur.close()

    return commitStatus

# function to display all orders to admin portal
def allorders(mysql,userID):
    cur = mysql.connection.cursor()
    cur.execute("SELECT o.orderID,o.customerID,o.bookID,o.quantity,o.total,o.timestamp,b.title FROM Orders as o, Books as b  WHERE o.bookID = b.bookID ORDER BY orderID")
    Data = list(cur.fetchall())
    mysql.connection.commit()
    cur.close()
    return Data

# function to display customers orders
def myorder(mysql,userID):
    cur = mysql.connection.cursor()
    cur.execute("SELECT o.bookID,o.quantity,o.total,o.timestamp,b.title FROM Orders as o,Books as b WHERE o.bookID = b.bookID AND o.customerID = %s",(userID,))
    Data = list(cur.fetchall())
    mysql.connection.commit()
    cur.close()
    return Data