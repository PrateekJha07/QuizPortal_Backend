#importing libraries
import sqlite3
import secrets
import csv,json
import quiz_creator

class Models: 
    def __init__(self):
        #creating instance of class from quiz_creator.py, paramaters(number of questions,quiz_id)
        self.quiz_create = quiz_creator.Quiz_creator(4,2)

    #functiont to add users
    def add_users(self,json_req):
        try:
            #connect to database
            conn = sqlite3.connect("Quiz.db")
            #create a hexadecimal token for users
            token_value = secrets.token_hex(5)
            #cursor for the DB
            cur=conn.cursor()
            #query to fetch admin's token 
            sql_query_admin= "SELECT token FROM users WHERE ID=%d"%(json_req["ID"])
            #Executing DB query 
            cur.execute(sql_query_admin)
            #storing value from the query
            rows = cur.fetchone()[0]
        except(TypeError):
            #Query to insert values in users table for admin
            sql_query = ("INSERT INTO users (ID,name,token) values(%d,%s,%s)" %(json_req["ID"],"'prateek'",json_req["token"]))
            #Executing DB query 
            cur.execute(sql_query)
            #commiting the changes made query
            conn.commit()
            #closing the database connection
            conn.close()
            #return values after adding admin
            return {"Status":200,"id":json_req["ID"],"Token":json_req["token"],"details":"Admin user is created"}
        else:
            #query to get count for rows from users table
            sql_query_full = "SELECT COUNT(*) FROM users"
            #Executing DB query 
            cur.execute(sql_query_full)
            #storing value from the query
            rows = cur.fetchone()[0]
            #condition to check the if DB is full
            if(int(rows)>10000):
                return "DB is full, No more users can be added."
            
            #query to add users other then admin in users table
            sql_query_token = "SELECT token FROM users WHERE ID=%d"%(json_req["ID"])
            #Executing DB query
            cur.execute(sql_query_token)
            #storing the value from the query
            rows_token=cur.fetchone()[0]
            #check the token to check if it matches that of the admin
            if(str(rows_token)==json_req["token"].replace("'","")):
                #Query to get max ID from users table
                sql_query_max = "SELECT MAX(ID) FROM users"
                #Executing DB query
                cur.execute(sql_query_max)
                #Storing the value of max ID
                rows_maxID = cur.fetchone()[0]
                #executing DB query to enter the details for user
                cur.execute("INSERT INTO users (ID,name,token) values(?,?,?)" ,(rows_maxID+1,"'Prateek'",str(token_value)))
                #Query to fetch token for the user
                sql_query_Usertoken = "SELECT token FROM users WHERE ID=%d"%(rows_maxID+1)
                #Executing DB query
                cur.execute(sql_query_Usertoken)
                #Storing the value of token from users
                rows_userToken = cur.fetchone()[0] 
                #commiting the changes made query
                conn.commit()
                #closing the database connection
                conn.close()
                #return values after adding users
                return {"Status":200,"ID":str(rows_maxID+1),"token":str(rows_userToken),"Details":"User added by Admin","errmsg":""}
            else:
                return "PLease login as Admin to add users." #return values if any user other than admin is trying to add users

    #function to delete users
    def delete_users(self,json_req):
        try:
            #connection for database
            conn = sqlite3.connect("Quiz.db")
            #create cursor for DB
            cur=conn.cursor()
            #Query to get token from users with user ID
            sql_query_token = "SELECT token FROM users WHERE id=%d"%(json_req["AdminID"])
            cur.execute(sql_query_token)
            rows_token = cur.fetchone()[0]
            #condition to check if the token extracted is admin's
            if(str(rows_token) == json_req["token"].replace("'","")):
                #query to get values from users with user ID
                sql_query_rows = ("SELECT * FROM users WHERE ID=%d"%(json_req["UserID"]))
                #execute DB query
                result = cur.execute(sql_query_rows)
                #store values fetched from query
                rows = cur.fetchone()[0]
            else:
                return "Please login as Admin to add users."            
        except(TypeError):
            #return if no user is found
            return "User does not exists, please create a admin/user to delete user."
        else:
            #query to delete users with user ID
            sql_query=("DELETE FROM users WHERE ID=%d"%(json_req["UserID"]))
            #execute DB query 
            cur.execute(sql_query)
            #commit change to the DB
            conn.commit()
            #close connection
            conn.close()
            #return values 
            return {"Details":"User deleted","Status":200,"Error msg":"","UserID":json_req["UserID"]}

    #function to add questions
    def add_questions(self,userID,json_req):
        try:
            #DB connection
            conn = sqlite3.connect("Quiz.db")
            #cursor for DB
            cur = conn.cursor()
            #query to get admin from users
            sql_query_admin = "SELECT * FROM users WHERE ID=%d"%(userID)
            #execute DB query
            cur.execute(sql_query_admin)
            #store value fetched from query
            rows = cur.fetchone()[0]
        except(TypeError):
            #return if admin does not exists
            return "Please create an admin to add questions."
        else:
            #query to get count of questions
            sql_query_full = "SELECT COUNT(*) FROM questions"
            cur.execute(sql_query_full)
            rows = cur.fetchone()[0]
            if(int(rows)>1000): #if to check whether DB is full?
                #return if DB is full
                return "DB is full, No more questions can be added."
            #query to fetch token from user ID
            sql_query_token = "SELECT token FROM users WHERE ID=%d"%(userID)
            cur.execute(sql_query_token)
            rows_token=cur.fetchone()[0]
            #condition to check if the token extracted is admins
            if(str(rows_token)==json_req["token"].replace("'","")):
                #Query to get max ID from questions table
                sql_query_maxID = "SELECT MAX(question_id) FROM questions"
                cur.execute(sql_query_maxID)
                rows_id = cur.fetchone()[0]
                #condition to check if any is extracted
                if(rows_id == None):
                    #query to add first question if no ID is present
                    try:
                        sql_query = "INSERT INTO questions (question_id,question,choice1,choice2,choice3,choice4,key,marks,remarks) values(%d,%s,%s,%s,%s,%s,%d,%d,%s)"%(1,json_req["question"],json_req["optionA"],json_req["optionB"],json_req["optionC"],json_req["optionD"],json_req["key"],json_req["marks"],json_req["remarks"])
                        cur.execute(sql_query)
                    except Exception as e:
                        return str(e)
                    else:
                        conn.commit()
                        conn.close()
                        #return value after adding the first questions 
                        return {"Status":200,"Details":"The first question is added to the DB","Question_id":rows_id+1}
                    finally:
                        conn.close()
                else:
                    #Query to add next question if ID is extracted
                    try:
                        sql_query = "INSERT INTO questions (question_id,question,choice1,choice2,choice3,choice4,key,marks,remarks) values(%d,%s,%s,%s,%s,%s,%d,%d,%s)"%(rows_id+1,json_req["question"],json_req["optionA"],json_req["optionB"],json_req["optionC"],json_req["optionD"],json_req["key"],json_req["marks"],json_req["remarks"])
                        cur.execute(sql_query)
                    except Exception as e:
                        return str(e)
                    else:
                        conn.commit() 
                        conn.close()
                        #return values
                        return {"Status":200,"Details":"The question is added to the DB","Question_id":rows_id+1}
                    finally:
                        conn.close()
        finally:
            #close connection to the DB
            conn.close()

    def delete_questions(self,json_req):
        try:
            #connection to the DB
            conn = sqlite3.connect("Quiz.db")
            cur = conn.cursor()
            #Query to get questions from question ID
            sql_query_question = "SELECT * FROM questions WHERE question_id=%d"%(json_req["ques_id"])
            cur.execute(sql_query_question)
            cur.fetchone()[0]
        except(TypeError):
            #return if no question was extracted
            return "The question is not present in the DB, please try with another ID."
        else:
            #Query to get token from users with user ID
            sql_query_token = "SELECT token FROM users WHERE id=%d"%(json_req["userID"])
            cur.execute(sql_query_token)
            rows_token = cur.fetchone()[0]
            #condition to check if the token extracted is admin's
            if(str(rows_token) == json_req["token"].replace("'","")):
                #Query to delete questions 
                sql_query_delques = "DELETE FROM questions WHERE question_id=%d"%(json_req["ques_id"])
                cur.execute(sql_query_delques)
                conn.commit()
                conn.close()
                #return values
                return {"Status":200,"Details":"The question was successfully deleted.","Ques_id":(json_req["ques_id"])}
            else:
                #return values if the token do not match
                return "Sorry, the token of the questions does not match to that of the admin, only admin can delete questions, please enter the correct token and try again."

    #function to get quiz after creating the quiz
    def create_quiz(self,json_req):
        try:
            #assigning values to return values from formulate() function in quiz_create.py
            final_questions,final_keys,final_questionsRowIDs,choice1,choice2,choice3,choice4,marks=self.quiz_create.formulate()
            #assigning value to return value from render()function in quiz_create.py
            dict_quiz = self.quiz_create.render()
            #connection to DB 
            Conn = sqlite3.connect("Quiz.db")
            curr = Conn.cursor()
            #Query to get token
            sql_query_token = "SELECT token FROM users WHERE ID=%d"%(json_req["userID"])
            curr.execute(sql_query_token)
            rows_token=curr.fetchone()[0]
        except Exception as e:
            return str(e) #return statement for exception
        else:
            #condition to check if the token extracted is active
            if(str(rows_token)==json_req["token"].replace("'","")):
                #Query to get questions from quiz
                sql_query_question = "SELECT questions FROM quiz WHERE quiz_id=%d"%(json_req["quiz_id"])
                curr.execute(sql_query_question)
                row_questions = curr.fetchall()
                #conditiont to check if the value is empty
                if(row_questions==[]):
                    #commiting changes to the DB
                    Conn.commit()
                    Conn.close()
                    #return values 
                    return "There are no questions present for the mentioned quiz id."
                else:    
                    Conn.commit()
                    Conn.close()
                    #return values
                    return dict_quiz
            else:
                #return values if user is not active
                return "The token do not match, the user is inactive. Please with a different ID."

    def get_score(self,json_req):
        try:
            #connection to DB
            conn = sqlite3.connect("Quiz.db")
            curr = conn.cursor()
            #Query to get token from ID
            sql_query_token = "SELECT token FROM users WHERE ID=%d"%(json_req["userID"])
            curr.execute(sql_query_token)
            rows_token=curr.fetchone()[0]
        except Exception as e:
            return str(e) #return exception if no values are extracted
        else:
            #condition to check if the token extracted is active
            if(str(rows_token)==json_req["token"].replace("'","")):
                #query to get values from quiz table using quiz_id
                sql_query_quesId = "SELECT * FROM quiz WHERE quiz_id=%d"%(json_req["quiz_id"])
                curr.execute(sql_query_quesId)
                rows_getdata = curr.fetchone()
                #condition to check if the values are none
                if(rows_getdata==None):
                    conn.commit()
                    conn.close()   
                    #return values
                    return {"Status":400,"Details":"Quiz with the ID is not created.","Quiz_ID":json_req["quiz_id"]}
                else:
                    #assigning value to return values from sort_method in quiz_create.py
                    score_output = self.quiz_create.sort_method()
                    #return the assigned value
                    return score_output
            else:
                #return value if token do not match
                return "The token do not match, the user is inactive. Please with a different ID."
