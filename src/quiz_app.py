#importing libraries
from flask import Flask,jsonify,request,session
import models

#creating a flask instance
app = Flask(__name__)

app.config['JSON_SORT_KEYS']=False

@app.route("/",methods=["POST","GET","DELETE"]) #defining route to homepage
def home():
    if(request.method=="GET"): #check the type of request
        data = request.get_json() #create a json object
        return data # return the value 
    else:
        return "Enter a valid request." #return value if request is not valid

@app.route("/users/",methods=["POST","GET"]) #defining route to add users
def add_users():
    if(request.method=="POST"):  #check the type of request
        data = request.get_json() #create a json object
        if(data["ID"]<10000 or data["ID"]>11000): #if to check the value of ID
            return "Please enter an ID between 10000-11000.\n" #return statement if ID not valid
        user_response = models.Models() #instance of class Models
        return jsonify(user_response.add_users(data)) #return the value for add_users function in Models
    else:
        return "please enter a valid response.\n" #return value if request is not valid

@app.route("/users/",methods=["POST","GET","DELETE"]) #route to delete users
def delete_users():
    if(request.method=="DELETE"): #check the type of request
        data = request.get_json()
        if(data["AdminID"]==str(10000)): #check to see if user is admin
            return "User ID belongs to admin, admin connot be deleted, please enter another ID.\n"
        user_response = models.Models() #instance of class Models
        return jsonify(user_response.delete_users(data)) #return values from delete_users Models
    else:
        return "Please enter a valid request.\n" #return value if request is not valid

@app.route("/AddQuestion/<userID>",methods=["POST","GET","DELETE"]) #route to add questions
def add_questions(userID):
    if(request.method=="POST"): #check the type of request
        data = request.get_json() #create a json object
        if(int(userID) == 10000): #check to see if user is admin
            questions_response = models.Models() #instance of class Models
            #return values from add_questions in Models
            return jsonify(questions_response.add_questions(int(userID),data))
        else:
            return "Sorry, only admin can add questions, please login is admin.\n" #return value if user is not admin
    else:
        return "Please enter a valid request.\n" #return value id request is not valid

@app.route("/DelQuestion/",methods=["POST","GET","DELETE"]) #route to delete questions
def delete_questions():
    if(request.method=="DELETE"): #check the type of request
        data = request.get_json() #create a json object
        delete_question_response = models.Models() #instance of class Models
        #return values from delete_questions from Models
        return jsonify(delete_question_response.delete_questions(data))
    else:
        return "Please enter a valid request.\n" #return value if request is not valid

@app.route("/quiz/",methods=["POST","GET","DELETE"]) #route to get the created quiz
def create_quiz():
    if(request.method=="GET"): #check the type of request
        data = request.get_json() #create a json object
        create_quiz_response = models.Models() #instance of class Models
        #return values from create_quiz
        return jsonify(create_quiz_response.create_quiz(data))
    else:
        return "Please enter a valid request." #return value if request is not valid

#route to post answers for the quix created above
@app.route("/quizAnswers/",methods=["POST","GET","DELETE"]) 
def score():
    if(request.method=="POST"): #check the type of request
        data = request.get_json() #create a json object
        get_score = models.Models() #instance of class Models
        #return values from get_score()
        return jsonify(get_score.get_score(data))
    else:
        return "Please enter a valid response." #return value if request is not valid

#running the flask app
if __name__ == "__main__":
    app.run(debug=True)
