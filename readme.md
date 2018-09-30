# Python Application 

This application involves writing Python code to extract information about jobs, people 
and companies from data files and load them into a consistent SQL database. It is an 
example of an Extract-Transform-Load (ETL) task. 

You have been given the task of generating some normalised data on job postings given some
data files in different formats.   You are given:

* An HTML file downloaded from the Jobs! website that lists 50 jobs
* A CSV spreadsheet containing details of companies
* A CSV spreadsheet containing details of people 

The HTML job listing mentions the title of each job and
the company it is with.  The CSV companies list includes
the company name and some contact details including the name
of a contact person.   The CSV people list includes more complete
details of those contacts plus some other people.  Your task is to read the data from
all of these files and add it into an SQL database. 

The schema for the SQL database is provided for you in the file database.py. You can
 run this file to create the database.  Your code will then add data to it. Note that:

* The companies and people tables are related through the contact field. In the companies
table the value of contact should be the id of the corresponding person.
* The positions and companies tables are related through the company field. In the
positions table the value of company should be the id of the corresponding company.
* In the companies CSV file, contact names are given in full but in the people CSV
file they are split into first, last and middle names. You need to match up these
records.

## Useful Python Modules

Python has many useful modules for this task. You will want to look at:
* the __csv__ module for reading and writing CSV files
* the __bs4__ module (BeautifulSoup) for reading HTML files

and of course you will use the __sqlite3__ module for handling the database.

## Required Output

To show that you have completed the task successfully, you will generate a single CSV file
report that contains the following fields:
* company name
* position title
* company location
* contact first name
* contact last name
* contact email

There should be one row in your output CSV file for every job in the HTML file. 

You will also submit the code you have written to solve this problem.  Your code **must** use 
functions and every function **must** include a suitable docstring that describes 
what it does.  Each function should implement a logical part of the overall ETL process.

