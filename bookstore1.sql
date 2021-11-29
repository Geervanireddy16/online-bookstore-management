create database bookstore;
use bookstore;
show tables;

-- -------------------------------------------------- CUSTOMERS ---------------------------------------------------
create table Customers(
	customerID varchar(30) not null primary key,
	firstName varchar(20),
	lastName varchar(20),
	emailID varchar(50),
	password varchar(50),
	phone varchar(10),
	country varchar(25),
	state varchar(25),
	pincode int,
	address varchar(50)
);

select * from Customers;
-- -------------------------------------------------- ADMINS ---------------------------------------------------
create table Admins(
	adminID varchar(30) not null primary key,
	firstName varchar(20),
	lastName varchar(20),
	emailID varchar(50),
	password varchar(50),
	phone varchar(10)
);

Select * from Admins;
insert into Admins(adminID,firstName,lastName,emailID,password,phone) values('admin1','Sam','Jones','sam@gmail.com','abc123',1234567892);
insert into Admins(adminID,firstName,lastName,emailID,password,phone) values('admin2','Anu','Sharma','anu@gmail.com','abc1',3454567892);

-- -------------------------------------------------- BOOKS ------------------------------------------------------
create table Books(
	bookID int not null primary key,
	authorID int,
	publisherID int,
	title varchar(50),
	genre varchar(15),
	publicationYear int,
	price int
);
-- no of books written by a author
select count(authorID) from Books where authorID = 502;
select * from Books;
select * from Authors;
select * from Publishers;
alter table Books add foreign key (authorID) references Authors(authorID);
alter table Books add foreign key (publisherID) references Publishers(publisherID);

-- books data along with author fname and lname
select * from Books as b,Authors as a where b.authorID = a.authorID;

SELECT b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName  
FROM Books as b
INNER JOIN Authors as a
ON b.authorID = a.authorID  
ORDER BY bookID;  

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
insert into Books(bookID,authorID,publisherID,title,genre,publicationYear,price) values(13,501,7001,'Into Thin Air','Adventure',1964,568);

delete FROM Books where bookID = 16; 
-- displays distinct genre in books tables
select distinct genre from Books; 

-- -------------------------------------------------- AUTHORS ---------------------------------------------------
create table Authors(
  authorID int not null primary key AUTO_INCREMENT,
  firstName varchar(20),
  lastName varchar(20)
);
select * from Authors;

alter table Authors AUTO_INCREMENT=500;
insert into Authors(firstName,lastName) values('Robert','Stevenson');
insert into Authors(firstName,lastName) values('Jon','Krakauer');
insert into Authors(firstName,lastName) values('John','Green');
insert into Authors(firstName,lastName) values('Colleen','Hover');
insert into Authors(firstName,lastName) values('Jane','Austen');
insert into Authors(firstName,lastName) values('Gillian','Flynn');
insert into Authors(firstName,lastName) values('Peter','Straub');

 -- -------------------------------------------------- PUBLISHERS ------------------------------------------------
 create table Publishers(
  publisherID int not null primary key AUTO_INCREMENT,
  country varchar(25)
  );
  
select * from Publishers;
alter table Publishers AUTO_INCREMENT=7000;
insert into Publishers(country) values('India');
insert into Publishers(country) values('USA');
insert into Publishers(country) values('Australia');

update Publishers set country = 'UK' where publisherID = 7000; 

-- -------------------------------------------------- ContactUs ------------------------------------------------
 create table ContactUs(
  id int not null primary key AUTO_INCREMENT,
  firstName varchar(20),
  lastName varchar(20),
  emailID varchar(50),
  message varchar(500),
  timestamp datetime
  );

  select * from ContactUs;
  

-- SELECT publisherID from Publishers WHERE country = 'USA'; 

-- display books genre wise
SELECT DISTINCT genre from Books;

SELECT * from Books where genre = 'Adventure';


-- search by title
SELECT  b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName  FROM Books as b,Authors as a WHERE title LIKE '%g%' AND b.authorID = a.authorID;

-- search by genre
SELECT  b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName  FROM Books as b,Authors as a WHERE b.genre = 'Adventure' AND b.authorID = a.authorID;

-- search by author
SELECT  b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName  FROM Books as b,Authors as a WHERE a.firstName LIKE '%o%' AND b.authorID = a.authorID;
