import csv, json
import sqlite3

class Quiz_creator:
    def __init__(self,number_questions,quiz_id):
        #assigning values
        self.number_questions = number_questions
        self.quiz_id = quiz_id

    #function to get values and insert them is the quiz table
    def formulate(self):
        #empty lists to appned extracted from the table
        final_questionsRowIDs = []
        final_keys = []
        final_questions = []
        choice1 = []
        choice2 = []
        choice3 = []
        choice4 = []
        marks = []
        #connection to DB
        Conn = sqlite3.connect("Quiz.db")
        curr = Conn.cursor()
        #query to get number of questions specified by the user
        sql_query_getQuestionID = "SELECT question_id FROM questions LIMIT %d"%(self.number_questions)
        curr.execute(sql_query_getQuestionID)
        rows_questionIDs = curr.fetchall()

        #loop to appned row IDs to empty list
        for row in rows_questionIDs:
            remove_char = str(row).replace(",","").replace("(","").replace(")","")
            final_questionsRowIDs.append(remove_char)
        
        #queries to extract values from the database
        for ques_id in final_questionsRowIDs:
            #get keys from question table
            sql_query_getKeys = "SELECT key FROM questions WHERE question_id=%s"%(ques_id)
            curr.execute(sql_query_getKeys)
            row_keys=curr.fetchall()
            final_keys.append(row_keys)
            #get questions from questions table
            sql_query_getQuestions = "SELECT question from questions WHERE question_id=%d"%int(ques_id)
            curr.execute(sql_query_getQuestions)
            rows_questions = curr.fetchall()
            final_questions.append(rows_questions)
            #get choice1 from questions table
            sql_query_getchoice1 = "SELECT choice1 from questions WHERE question_id=%d"%int(ques_id)
            curr.execute(sql_query_getchoice1)
            rows_choice1 = curr.fetchall()
            choice1.append(rows_choice1) 
            #get choice2 from questions table
            sql_query_getchoice2 = "SELECT choice2 from questions WHERE question_id=%d"%int(ques_id)
            curr.execute(sql_query_getchoice2)
            rows_choice2 = curr.fetchall()
            choice2.append(rows_choice2)
            #get choice3 from questions table
            sql_query_getchoice3 = "SELECT choice3 from questions WHERE question_id=%d"%int(ques_id)
            curr.execute(sql_query_getchoice3)
            rows_choice3 = curr.fetchall()
            choice3.append(rows_choice3)
            #get choice4 from questions table
            sql_query_getchoice4 = "SELECT choice4 from questions WHERE question_id=%d"%int(ques_id)
            curr.execute(sql_query_getchoice4)
            rows_choice4 = curr.fetchall()
            choice4.append(rows_choice4) 
            #get marks from questions table
            sql_query_marks = "SELECT marks from questions WHERE question_id=%d"%int(ques_id)
            curr.execute(sql_query_marks)
            rows_marks = curr.fetchall()
            marks.append(rows_marks) 

        #Query to fetch the max ID from quiz
        sql_query_getID = "SELECT MAX(quiz_id) from quiz"
        curr.execute(sql_query_getID)
        rows_id = curr.fetchone()[0]
        #condition to check if the extracted in none
        if(rows_id==None):
            #executing the query to add values to the quiz
            curr.execute("INSERT INTO quiz (quiz_id,questions,answerkeys) values(?,?,?)",(rows_id,str(final_questions),str(final_keys)))
            Conn.commit()
            Conn.close()
            #return values extracted/appended in the above function
            return final_questions,final_keys,final_questionsRowIDs,choice1,choice2,choice3,choice4,marks
        else:
            #incremen the max row ID by 1
            rows_id+=1
            #executing the query to add values to the quiz
            curr.execute("INSERT INTO quiz (quiz_id,questions,answerkeys) values(?,?,?)",(rows_id,str(final_questions),str(final_keys)))
            #commiting changes to the DB
            Conn.commit()
            #closing connection to the DB
            Conn.close()
            #return values extracted/appended in the above function
            return final_questions,final_keys,final_questionsRowIDs,choice1,choice2,choice3,choice4,marks

    def render(self):
        #assigning value to return values from formulate()
        final_questions,final_keys,final_questionsRowIDs,choice1,choice2,choice3,choice4,marks = self.formulate()
        #creating an emplty dictionary
        dict_quiz = {}
        #Connection to DB
        conn = sqlite3.connect("Quiz.db")
        curr = conn.cursor()
        #empty list to append the score
        marks_score = []
        #loop to append marks_score list
        for i in range(len(final_questionsRowIDs)):
            marks_score.append(1)
        score = sum(marks_score) #calculating sum of the marks from list
        #loop to add values to the dict
        for i in range(len(final_questions)):
                temp_ques = {}
                temp_ques["Question"] = final_questions[i][0][0]
                temp_ques["choice1"] = choice1[i][0][0]
                temp_ques["choice2"] = choice2[i][0][0]
                temp_ques["Choice3"] = choice3[i][0][0]
                temp_ques["Choice4"] = choice4[i][0][0]
                temp_ques["Marks"] = marks[i][0][0]
                dict_quiz['q'+str(i+1)] = temp_ques
        #Insert into test instance
        sql_query_maxID = "SELECT MAX(id) FROM test_instance"
        curr.execute(sql_query_maxID)
        maxid = curr.fetchone()[0]
        #condition to check in max value is none
        if(maxid == None):
            #Query to enter the first value if max value is none
             curr.execute("INSERT INTO test_instance (id,quiz_id,user_id,answerkeys,score) values(?,?,?,?,?)",(100,self.quiz_id,10002,str(final_keys),score))
             conn.commit()
             conn.close()
             #return values as a dictionary
             return dict_quiz 
        else:
            #Query to enter values in test instance
            curr.execute("INSERT INTO test_instance (id,quiz_id,user_id,answerkeys,score) values(?,?,?,?,?)",(maxid+1,self.quiz_id,10002,str(final_keys),score))
            conn.commit() 
            conn.close()
            #return values as a dictionary
            return dict_quiz

    def sort_method(self):
        #assigning value to return values from formulate()
        final_questions,final_keys,final_questionsRowIDs,choice1,choice2,choice3,choice4,marks= self.formulate()
        #connection to the DB
        conn = sqlite3.connect("Quiz.db")
        curr = conn.cursor()
        #Answers entered by the user
        anwers = [1,2,1,2]
        #Final result list to enter the score
        result = []
        #final answer list to get the answers
        final_answers = []
        #condition to check in the answers entered is more than the questions asked
        if(len(anwers)>len(final_questionsRowIDs)):
            return "The answers are more than the questions. Please try again."
        else:
            #Query to get values from quiz table
            sql_query_quesId = "SELECT * FROM quiz WHERE quiz_id=%d"%(self.quiz_id)
            curr.execute(sql_query_quesId)
            rows_getdata = curr.fetchone()
            #condition to check if the value is none
            if(rows_getdata==None):
                conn.commit()
                conn.close()  
                #return the value if the data is none
                return {'Status':400,'Details':'Quiz with the ID is not created.','Quiz_ID':self.quiz_id}
            else:
                #loop to get key values from the questions table
                for ques_id in final_questionsRowIDs:
                    sql_query_keys = ("SELECT key FROM questions WHERE question_id=%d"%int(ques_id))
                    curr.execute(sql_query_keys)
                    rows_key=curr.fetchone()
                    #appending the final key to the list
                    final_answers.append(rows_key) 
                    if(rows_key==None): #if the key value is none
                        conn.commit()
                        #return key not found
                        return "Key was not found."
                    else:
                        #Commmit changes to the DB
                        conn.commit()
                #loop to compare the answer entered by the user and key from questions table
                for i in range(0,len(anwers)):
                    if(str(anwers[i])==str(final_answers[i][0])):
                        score = 1
                        result.append(score)
                    else:
                        score = 0
                        result.append(score)
                #Closing DB connection
                conn.close()
        #calculating the sum of the score
        score = sum(result)
        #return values to display
        return {'Score':score,'Result':str(result),'Status':200,'error_message':""}

    #this is to import the questions from CSV and enter it into the questions database
    def import_csv(self):
        #opening quiz.csv file
        file = open("quiz.csv")
        #Connection to the DB
        conn = sqlite3.connect("Quiz.db")
        cur = conn.cursor()
        #creaing instance of the csv file
        csvreader = csv.reader(file)
        #fetching the column headers from the file
        headers = next(csvreader)
        #loop to enter values to the questions table
        for row in csvreader:
            #query to enter values to the questions table
            sql_query = "INSERT INTO questions (question_id,question,choice1,choice2,choice3,choice4,key,marks,remarks) values(%d,%s,%s,%s,%s,%s,%d,%d,%s)"%(int(row[0]),row[1],row[2],row[3],row[4],row[5],int(row[6]),int(row[7]),row[8])
            #executing query
            cur.execute(sql_query)
            #Comitting changes to the DB
            conn.commit()
        #DB connection closed
        conn.close()    
        #file closed
        file.close()

#Uncomment these two statements to import the questions from CSV and upload to questions table
#import_obj = Quiz_creator(4,2)
#import_obj.import_csv()