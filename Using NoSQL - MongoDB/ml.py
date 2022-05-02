from pymongo import MongoClient
# from tabulate import tabulate
import numpy as np
from os import getenv
from dotenv import load_dotenv
load_dotenv()

# from sklearn import metrics
# sakjiflks
db_link = getenv('MONGO',None)
db_name = getenv('DB_NAME',None)

client = MongoClient(db_link)
db = client.get_database(db_name)


X=[]
y=[]
booksData = db.books.find({'genre':'adventure'})
for book in booksData:
    X.append(int(book['bookID']))
    y.append([0])

booksData1 = db.books.find({'genre':'mystery'})
for book in booksData1:
    X.append(int(book['bookID']))
    y.append([1])

# X = X.reshape(-1,1)
# print(tabulate(X, headers='firstrow'))
# print("\n")
# print(tabulate(Y, headers='firstrow'))
print(X)
x = np.append(X)
print(x)
from sklearn.model_selection import cross_val_score

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20) #0.20 means 80% from training and 20% for testing

# from sklearn.svm import SVC
# svclassifier = SVC(kernel='linear')
# svclassifier.fit(X_train, y_train)