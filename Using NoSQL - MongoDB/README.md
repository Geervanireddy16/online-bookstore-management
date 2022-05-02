# Online BookStore Management Application
To open deployed app [click here.](https://onlinebookstoree.herokuapp.com/)
 
## Technology Stack
* **Frontend:** [HTML](https://html.com/), [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS), [Bootstrap](https://getbootstrap.com/), [Javascript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
* **Backend:** [Python Flask](https://flask.palletsprojects.com/en/2.0.x/)
* **Database:** [MongoDB](https://www.mongodb.com/atlas/database)

## Requirements
* [Visual Studio Code](https://code.visualstudio.com/)
* [MongoDB Atlas Account](https://www.mongodb.com/atlas/database)
* [Python](https://www.python.org/)
* [Flask](https://pypi.org/project/Flask/)
    1. pip install flask  
    2. pip install python-dotenv (to load the mongo details from env file to the required file)
    3. pip install gunicorn (for deploying on heroku)
* [Heroku Account](https://signup.heroku.com/)
* [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli)

## Website Preview
[Click here](https://github.com/Geervanireddy16/online-bookstore-management/blob/main/README.md)

## Project Structure
    .
    ├── static          
    |   └── bootstrap
    |   └── css
    |   └── images
    |   └── js
    ├── templates                   # html files 
    ├── utils                       # code files
    ├── app.py              
    ├── mongoqueries.txt      # queries and triggers code
    ├── .gitignore
    ├── .env
    ├── Procfile              # tells Heroku how to startup your application on it's servers
    ├── requirements.txt
    └── README.md

## Triggers
Trigger is a code which is automatically executed in response to certain events on a particular document in a monogdb database.
For our application, we have created 2 triggers which is enabled as soon as a document is inserted in *orders* collection (ie an order has been placed by the user)
1. IncSoldStock - Increment sold stock count by the quantity ordered by the user.
2. DcrTotalStock - Decrement total stock count by the quantity ordered by the user.

>Note: *IncSoldStock* and *DcrTotalStock* are the trigger names.

### Steps to create a trigger
1. Name the trigger and enable event ordering
2. Link Datasource to the database (in our case, its is Cluster0)
3. In Trigger source details, type the cluster name, database name, collection name (for our application its *orders*) and operation type is insert. Enable full document.
4. Function code for *IncSoldStock* Trigger
  ```bash
      exports = function(changeEvent) {
        const fullDocument = changeEvent.fullDocument;
        const bookID = fullDocument.bookID;
        const quantity = fullDocument.quantity;
        const book_collection = context.services.get("Cluster0").db("bookstore").collection("books");
        
        const doc = book_collection.updateOne(           
          {bookID: bookID},
          {"$inc": {"soldStock": quantity}}
        );
        return doc;
      };
```

5. Function code for *DcrTotalStock* Trigger
  ```bash
    exports = function(changeEvent) {
      const fullDocument = changeEvent.fullDocument;
      const bookID = fullDocument.bookID;
      const quantity = fullDocument.quantity;
      const book_collection = context.services.get("Cluster0").db("bookstore").collection("books");
      
      const doc = book_collection.updateOne(          
        {"bookID": bookID},
        {"$inc": {"totalStock": -quantity}}
      );
      return doc;
    };
```


## Steps to deploy our application on Heroku
1. Heroku login
2. Install gunicorn (Ignore if previously installed)
  ```bash
    pip install gunicorn
  ```

3. Generate requirements file
  ```bash
  pip freeze > requirements.txt
  ```

4. Create a Procfile
  ```bash
    web: gunicorn app:app
  ```
>Note : *web* is used by Heroku to start a web server for our application. The *app:app* specifies the module and application name. In our application we have the app module and our flask application is also called app.

5. Heroku Login (in browser) and create an app
>Note: *onlinebookstoree* is the name of our app

6. Heroku Login (in terminal)
  ```bash
    heroku login
  ```
    
6. Create a git repository
  ```bash
    git init
    heroku git:remote -a onlinebookstoree
  ```
>Note: For existing git repository use *heroku git:remote -a onlinebookstoree*

7. Deploy our application
  ```bash
    git add .
    git commit -m “message”
    git push heroku main
```
