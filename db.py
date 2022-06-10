import sqlite3

#connect to to database
conn = sqlite3.connect("users.sqlite")

#The sqlite3.Cursor class is an instance using which you can invoke methods that execute SQLite statements,
cursor = conn.cursor()
sql_query = """ CREATE TABLE user(
    user_id INTEGER PRIMARY KEY,
    full_name VARCHAR(30) NOT NULL,
    email VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    position VARCHAR(50) NULL,
    south_african_id VARCHAR(14) NOT NULL
)"""

sql_query2 = """ CREATE TABLE submissionPeriod(
    sub_id INTEGER PRIMARY KEY,
    submit_from_date TEXT,
    submit_to_date TEXT,
    financial_year TEXT NOT NULL
)"""

cursor.execute(sql_query)
conn.close()