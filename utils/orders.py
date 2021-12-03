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