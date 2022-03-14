import sqlite3

conn = sqlite3.connect("Quiz.db") #create or open the FILE
cur = conn.cursor()
sql_query = "CREATE TABLE users(ID integer PRIMARY KEY,name varchar(255),token varchar(255))"
cur.execute(sql_query)

sql_query = "create table questions (question_id integer PRIMARY KEY, question varchar(1000) unique,choice1 varchar(255), choice2 varchar(255), choice3 varchar(255), choice4 varchar(255), key integer, marks integer, remarks varchar(255))"
cur.execute(sql_query)

sql_query = "create table quiz(quiz_id integer PRIMARY KEY, questions varchar(2000),answerkeys varchar(255))"
cur.execute(sql_query)

sql_query = "create table test_instance(id integer PRIMARY KEY, quiz_id integer REFERENCES quiz(quiz_id), user_id integer REFERENCES users(ID), answerkeys varchar(255), score integer)"
cur.execute(sql_query)

conn.commit() #journaling

conn.close() #write to fil