"""
Module to read data from CSV files and HTML file
to populate an SQL database

ITEC649 2018
"""

import sys
import csv
import sqlite3
from database import DATABASE_NAME
from bs4 import BeautifulSoup


#Exceute this to read the html file and create CSV
def create_csv_from_html():
    soup = BeautifulSoup(open("index.html"), 'html.parser')
    jobs = soup.find_all('div', attrs={"class": "card-header"})


    positions=[]
    orgs=[]
    for job in jobs:
        position = job.find('h5', attrs={'class':'card-title'}).text
        org = job.find('div', attrs={'class':'company'}).text
        positions.append(position)
        orgs.append(org)


    with open("positions.csv", "w") as csvfile:
        columnTitleRow = "job,company\n"
        csvfile.write(columnTitleRow)
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerows(zip(positions, orgs))


#Execute this to create peoples table table
def insert_people_data():
    db = sqlite3.connect(DATABASE_NAME)
    cur = db.cursor()
    with open('people.csv','rt',encoding="utf-8") as fin:
        dr = csv.DictReader(fin)
        to_db = [(i['person_ID'], i['first'],i['last'],i['middle'],i['email'],i['phone']) for i in dr]
        cur.executemany("INSERT INTO people (id, last_name, first_name, middle_name, email, phone) VALUES (?, ?, ?, ?, ?, ?);", to_db)
    db.commit()
    db.close()

# Execute this to create companies table
def insert_companies_data():
    db = sqlite3.connect(DATABASE_NAME)
    cur = db.cursor()
    with open('companies.csv','rt',encoding="utf-8") as fin:
        dr = csv.DictReader(fin)
        to_db = [(i['company'],i['location'],i['contact'], i['url']) for i in dr]
        cur.executemany("INSERT INTO companies (companies_name,location,name,url) VALUES (?,?,?,?);", to_db)
    db.commit()
    db.close()

# Execute this to update contact in companies table
def update_companies_data():
    db = sqlite3.connect(DATABASE_NAME)
    cur = db.cursor()
    cur.execute("""
    update companies set contact =
    (select people.id from people where people.first_name =
    substr(companies.name,1,5)) where exists( select * from people where people.first_name
    = substr(companies.name,1,5));""")

    db.commit()
    db.close()

# Execute this to create positions table
def insert_positions_data():
    db = sqlite3.connect(DATABASE_NAME)
    cur = db.cursor()
    with open('positions.csv','rt',encoding="utf-8") as fin:
        dr = csv.DictReader(fin)
        to_db = [(i['job'], i['company']) for i in dr]
        cur.executemany("INSERT INTO positions (title,company_name) VALUES (?,?);", to_db)
        db.commit()
        db.close()

def create_final_csv():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    conn.row_factory = sqlite3.Row
    crsr = conn.execute("select distinct companies.companies_name,positions.title,companies.location,people.first_name, people.last_name,people.email from people INNER JOIN companies ON people.id = companies.contact INNER JOIN positions on companies.companies_name = positions.company_name;")
    row = crsr.fetchone()
    titles = row.keys()

    data = c.execute("select distinct companies.companies_name,positions.title, companies.location,people.first_name,people.last_name,people.email from people INNER JOIN companies ON people.id = companies.contact INNER JOIN positions on companies.companies_name = positions.company_name;")
    if sys.version_info < (3,):
        f = open('output.csv', 'wb')
    else:
        f = open('output.csv', 'w', newline="")

    writer = csv.writer(f, delimiter=',')
    writer.writerow(titles)  # keys=title you're looking for
    # write the rest
    writer.writerows(data)
    f.close()



if __name__=='__main__':

    create_csv_from_html()
    db = sqlite3.connect(DATABASE_NAME)
    insert_people_data()
    insert_companies_data()
    update_companies_data()
    insert_positions_data()
    create_final_csv()












