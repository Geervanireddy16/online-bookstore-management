create database onlinebookstore;
use onlinebookstore;
show tables;
-- drop database onlinebookstore; 

-- -----------------------------------------------------TABLES-----------------------------------------------------------------------------
create table Customers(
	customerID varchar(30) primary key,
	firstName varchar(20),
	lastName varchar(20),
	emailID varchar(50),
	password varchar(30),
	phone varchar(10),
	country varchar(25),
	state varchar(25),
	pincode int,
	address varchar(50)
);

create table Admins(
	adminID varchar(30) primary key,
	firstName varchar(20),
	lastName varchar(20),
	emailID varchar(50),
	password varchar(30),
	phone varchar(10)
);

create table Books(
	bookID int primary key,
	authorID int,
	publisherID int,
	title varchar(50),
	genre varchar(15),
	publicationYear int,
	price int
);

create table Authors(
  authorID int primary key AUTO_INCREMENT,
  firstName varchar(20),
  lastName varchar(20)
);

create table Publishers(
  publisherID int primary key AUTO_INCREMENT,
  country varchar(25)
  );
  
create table Inventory(
   bookID int primary key,
   totalStock int,
   soldStock int
);

create table Orders(
  orderID int AUTO_INCREMENT,
  customerID varchar(30),
  bookID int,
  quantity int not null,
  total	int,
  timestamp datetime,
  primary key(orderID,customerID,timestamp,bookID)
);

create table Payment(
  paymentID int primary key AUTO_INCREMENT,
  customerID varchar(30),
  paymentInfo int not null
);

create table ContactUs(
  id int primary key AUTO_INCREMENT,
  firstName varchar(20),
  lastName varchar(20),
  emailID varchar(50),
  message varchar(1000),
  timestamp datetime
  );
  
  -- -----------------------------------------------------ALTER TABLE -----------------------------------------------------------------------------
alter table Authors AUTO_INCREMENT=500;
alter table Publishers AUTO_INCREMENT=7000;
  
  -- -----------------------------------------------------FOREIGN KEYS-----------------------------------------------------------------------------
  
  -- Foreign Keys in Books Table
alter table Books add foreign key (authorID) references Authors(authorID);
alter table Books add foreign key (publisherID) references Publishers(publisherID);

-- Foreign Key in Inventory 
alter table Inventory add foreign key (bookID) references Books(bookID);

-- Foreign Keys in Orders 
alter table Orders add foreign key (customerID) references Customers(customerID); 

-- Foreign Keys in Payment
alter table Payment add foreign key (customerID) references Customers(customerID); 


 -- -----------------------------------------------------INSERT INTO TABLE -----------------------------------------------------------------------------
 
 -- Admins
insert into Admins(adminID,firstName,lastName,emailID,password,phone) values('admin1','Sam','Jones','sam@gmail.com','abc123',1234567892);
insert into Admins(adminID,firstName,lastName,emailID,password,phone) values('admin2','Anu','Sharma','anu@gmail.com','abc1',3454567892);
 
 
 -- Authors
insert into Authors(firstName,lastName) values('Robert','Stevenson');
insert into Authors(firstName,lastName) values('Jon','Krakauer');
insert into Authors(firstName,lastName) values('John','Green');
insert into Authors(firstName,lastName) values('Colleen','Hover');
insert into Authors(firstName,lastName) values('Jane','Austen');
insert into Authors(firstName,lastName) values('Gillian','Flynn');
insert into Authors(firstName,lastName) values('Peter','Straub');

-- Publishers
insert into Publishers(country) values('UK');
insert into Publishers(country) values('USA');
insert into Publishers(country) values('Australia');
 
 -- Books
insert into Books(bookID,authorID,publisherID,title,genre,publicationYear,price) values(1,500,7000,'Treasure Island','Adventure',1964,345);
insert into Books(bookID,authorID,publisherID,title,genre,publicationYear,price) values(2,500,7000,'Life of Pi','Adventure',2001,295);
insert into Books(bookID,authorID,publisherID,title,genre,publicationYear,price) values(3,506,7001,'Black House','Horror',2001,800);
insert into Books(bookID,authorID,publisherID,title,genre,publicationYear,price) values(4,506,7001,'Ghost Story','Horror',1979,499);
insert into Books(bookID,authorID,publisherID,title,genre,publicationYear,price) values(5,505,7001,'The Grownup','Horror',2015,99);
insert into Books(bookID,authorID,publisherID,title,genre,publicationYear,price) values(6,505,7001,'Gone Girl','Mystery',2012,367);
insert into Books(bookID,authorID,publisherID,title,genre,publicationYear,price) values(7,502,7001,'Paper Towns','Mystery',2008,199);
insert into Books(bookID,authorID,publisherID,title,genre,publicationYear,price) values(8,502,7001,'Fault in our Stars','Romance',2012,687);
insert into Books(bookID,authorID,publisherID,title,genre,publicationYear,price) values(9,503,7001,'Layla','Mystery',2020,1598);
insert into Books(bookID,authorID,publisherID,title,genre,publicationYear,price) values(10,503,7001,'Ugly Love','Romance',2014,350);
insert into Books(bookID,authorID,publisherID,title,genre,publicationYear,price) values(11,504,7000,'Pride & Prejudice','Romance',1813,295);
insert into Books(bookID,authorID,publisherID,title,genre,publicationYear,price) values(12,504,7000,'Mysteries of Udolpho','Mystery',1793,795);
insert into Books(bookID,authorID,publisherID,title,genre,publicationYear,price) values(13,501,7002,'Into Thin Air','Adventure',1964,568);

-- Inventory
insert into Inventory (bookID,totalStock,soldStock) values (1,100,0);
insert into Inventory (bookID,totalStock,soldStock) values (2,100,0);
insert into Inventory (bookID,totalStock,soldStock) values (3,100,0);
insert into Inventory (bookID,totalStock,soldStock) values (4,100,0);
insert into Inventory (bookID,totalStock,soldStock) values (5,100,0);
insert into Inventory (bookID,totalStock,soldStock) values (6,100,0);
insert into Inventory (bookID,totalStock,soldStock) values (7,100,0);
insert into Inventory (bookID,totalStock,soldStock) values (8,100,0);
insert into Inventory (bookID,totalStock,soldStock) values (9,100,0);
insert into Inventory (bookID,totalStock,soldStock) values (10,100,0);
insert into Inventory (bookID,totalStock,soldStock) values (11,100,0);
insert into Inventory (bookID,totalStock,soldStock) values (12,100,0);
insert into Inventory (bookID,totalStock,soldStock) values (13,100,0);

-- -----------------------------------------------------SELECT -----------------------------------------------------------------------------
select * from Admins;
select * from Customers;
select * from Authors;
select * from Publishers;
select * from Inventory;
select * from Books;
select * from Orders;
select * from Payment;
select * from ContactUs;

-- Login Customers
SELECT * from Admins 
WHERE adminID = '' AND password = '';

-- Login Admins
SELECT * from Customers 
WHERE customerID = '' AND password = '';

-- Get Book,Authors Information from Books and Authors Table
SELECT b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName 
FROM Books as b INNER JOIN Authors as a ON b.authorID = a.authorID  
ORDER BY bookID;

-- Display book,author,publihsers details from Books,Authors and Publishers table by booksID
SELECT b.bookID,b.title,b.genre,b.price,b.publicationYear,a.firstName,a.lastName,p.country 
FROM Books as b 
JOIN Authors as a ON b.authorID = a.authorID 
JOIN Publishers as p on b.publisherID = p.publisherID 
WHERE b.bookID = '';

-- get distinct genre from Books Table
SELECT DISTINCT genre from Books;

-- Select PublisherID from country in Publishers Table
SELECT publisherID from Publishers 
WHERE country = '';

-- Select authorID from Authors name in Authors Table
SELECT authorID from Authors 
WHERE firstName = '' AND lastName = '';

-- Count number of books published by author
SELECT count(authorID) from Books WHERE authorID = '';

-- Count number of books pubished by a specific country
SELECT count(authorID) FROM Books WHERE publisherID = '';

-- Display book stock from Inventory table
SELECT b.bookID,b.title,i.totalStock,i.soldStock 
FROM Books as b,Inventory as i WHERE b.bookID=i.bookID;

-- Display books price,id and title from Books table
SELECT bookID,price,title from Books where bookID = '';

-- Search books by book title
SELECT b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName 
FROM Books as b,Authors as a 
WHERE title LIKE '%  %' AND b.authorID = a.authorID;

-- Search books by book author's first name
SELECT b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName 
FROM Books as b,Authors as a 
WHERE a.firstName LIKE '% %' AND b.authorID = a.authorID;

-- Search books by book author's last name
SELECT b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName 
FROM Books as b,Authors as a 
WHERE a.lastName LIKE '% %' AND b.authorID = a.authorID;

-- Search books by book genre
SELECT b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName 
FROM Books as b, Authors as a 
WHERE b.genre LIKE '% %' AND b.authorID = a.authorID;

-- Display admin account
SELECT * from Admins WHERE adminID = '';

-- Display customer account
SELECT * from Customers WHERE customerID = '';

-- Display all orders in admins account
Select o.orderID,o.customerID,o.bookID,b.title,o.quantity,o.total,o.timestamp
FROM Orders as o, Books as b 
WHERE o.bookID = b.bookID ORDER BY orderID;

-- Display orders by userID
Select o.bookID,b.title,o.quantity,o.total,o.timestamp
FROM Orders as o,Books as b
WHERE o.bookID = b.bookID AND o.customerID = 'geervaniii';
-- -----------------------------------------------------INSERT -----------------------------------------------------------------------------

-- Register Customers
INSERT INTO Customers(customerID,firstName,lastName,address,pincode,country,phone,state,emailID,password) 
VALUES ('','','','','','','','','','');

-- Insert new country in Publishers Table
INSERT INTO Publishers(country) VALUES ('');

-- Insert new author in Authors Table
INSERT INTO Authors(firstName,lastName) VALUES ('','');

-- Insert book in Books table
INSERT INTO Books(bookID,authorID,publisherID,title,genre,publicationYear,price) 
VALUES ('','','','','','','');

-- Insert book stock in Inventory table
INSERT INTO Inventory (bookID,totalStock,soldStock) VALUES('','','');

-- Insert into contact us form
INSERT INTO ContactUs(firstName,lastName,emailID,message,timestamp) 
VALUES ('','','','','');

-- Insert Orders
INSERT into Orders(customerID,bookID,quantity,total,timestamp) 
values('','','','','');

-- Insert Payments
INSERT into Payment(customerID,paymentInfo) 
values ('','');


-- ----------------------------------------------------- UPDATE -----------------------------------------------------------------------------
-- Update Book Price in Books table
UPDATE Books SET price = '' WHERE bookID = '' AND authorID = '' AND publisherID  = '' AND price = '';

-- Update sold books in Inventory table
UPDATE Inventory set soldStock = soldStock + '' where bookID = '';

-- Update total books in Inventory table
UPDATE Inventory set totalStock = totalStock - '' where bookID = '';

-- ----------------------------------------------------- DELETE -----------------------------------------------------------------------------
-- Delete author from Authors table
DELETE FROM Authors WHERE authorID = ''; 

-- Delete publisher country from Publihsers table
DELETE FROM Publishers WHERE publisherID ='';

-- Delete book stock from Inventory table
DELETE FROM Inventory WHERE bookID = '';

-- Delete books from Books table
DELETE FROM Books WHERE bookID = '';

-- ----------------------------------------------------- TRANSACTION -----------------------------------------------------------------------------
call temp()

DELIMITER $$
create PROCEDURE temp()
BEGIN
	DECLARE _rollback BOOL default 0;
    DECLARE CONTINUE HANDLER FOR 1051 SET _rollback=1;
    DECLARE CONTINUE HANDLER FOR 1048 SET _rollback=1;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET _rollback=1;
	START TRANSACTION;
		INSERT into Orders(customerID,bookID,quantity,total,timestamp) values('','','','','');
        UPDATE Inventory set soldStock = soldStock + '' where bookID = '';
        UPDATE Inventory set totalStock = totalStock + '' where bookID = '';
        INSERT into Payment(customerID,paymentInfo) values ('',''); --  throws error if pyamentInfo is incorrect
		if _rollback = 1 then
			rollback;
		else
			commit;
		end if;
END $$
DELIMITER ;