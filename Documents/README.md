This project is a complete backend implemenation for a quiz portal web app.

A person can perform the following tasks in the website:
1. show URLs used in the quiz portal
2. Add users and one admin
3. Verify the token(unique identifications) of users and admin
4. Admin can delete users, users cannot delete other users
5. Only admin can add questions
6. Only admin can delete questions
7. Users can create a quiz of specified number of questions 
8. Users can submit the answers and get the final score

deployment instruction:
To setup the database:
1. run quiz_app_setup.py
    python3 quiz_app_setup.py -> run this file to import questions from CSV after initializing the instances 
To run the project use the following command
1. python3 quiz_app.py
After starting the flask application
1. Use curl, the commands present in API documentation (zipped along with other files) to run the various API being in the website

Project folder structure:
All the API/JSON are placed under the API folder
API:
    -adminDetails.json
    -deleteQuestions.json
    -question.json
    -quiz.json
    -quizAnswers.json
    -URLs.json
