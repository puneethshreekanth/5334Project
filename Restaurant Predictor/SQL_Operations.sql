/* Create a database for the project*/
create database dmfinal2;

/*Use the Database*/
use dmfinal2;

/*Create Business table*/
create table business(
city varchar(30), 
review_count int,
name varchar(100), 
neighborhoods varchar(30),
type varchar(30), 
business_id varchar(25) primary key,
full_address varchar(500), 
hours varchar(1000), 	
state varchar(5), 
longitude float,
stars float, 
latitude float, 
attributes varchar(2000), 
open varchar(20),
categories varchar(1000));
/* Load the data from CSV file to Business Table*/
load data local infile 'C:\\Shree\\Study\\Data Mining\\Course_Project\\CSV_Files\\yelp_academic_dataset_business_clean.json'
into table business
fields terminated by '\t'
lines terminated by '\n';

/*Create Review table*/
create table review(
funny int, 
useful int, 
cool int,
user_id varchar(25), 
review_id varchar(25), 
text text, 
business_id varchar(25), 
stars int, 
date date,
type varchar(50));

/* Load the data from CSV file to Review Table*/
load data local infile 'C:\\Shree\\Study\\Data Mining\\Course_Project\\CSV_Files\\yelp_academic_dataset_review_clean.json'
into table review
fields terminated by '\t'
lines terminated by '\n';

/*Create User table*/
create table user(
yelping_since varchar(10),
funny int, 
useful int,
cool int, 
user_id varchar(25) , 
name varchar(50), 
elite varchar(300), 
type varchar(20), 
compliments varchar(300), 
fans int, 
average_stars float, 
review_count int, 
friends text);


/* Load the data from CSV file to User Table*/
load data local infile 'C:\\Shree\\Study\\Data Mining\\Course_Project\\CSV_Files\\yelp_academic_dataset_user_clean.json'
into table user
fields terminated by '\t'
lines terminated by '\n';

/*Query Used to get the User, his review and corresponding Business data to Pass to KNN*/
select distinct concat((REPLACE(REPLACE(categories, '\r', ''), '\n', '')),' ') category, (REPLACE(REPLACE(attributes, '\r', ''), '\n', '')) attributes,b.business_id,user_id,concat(b.name,' ') name,b.review_count,b.stars,b.longitude,b.latitude
from review r, business b
where r.business_id = b.business_id
and categories LIKE '%Restaurants%'
and user_id like '%ZIaaMdfsTFdwFZejaGf1tw%';

/*Save the query result to User_Review_att.csv*/


