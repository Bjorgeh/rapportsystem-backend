#Imports libs
from flask import Flask, jsonify, request, render_template
import os

#imports SQL Connection function
from SQLConnections import SQL_CreateNewUser

#prints current working directory
print(os.getcwd())

#Init app
app = Flask(__name__)

@app.route('/api', methods=['GET'])
def documentation():
    return render_template('documentation.html', name="Documentation")

#Get /test - data
@app.route('/test', methods=['GET'])
def testGet():
    #Returns set value
    
    #data = {"email": "test@epost.com", "userPass": "testPass", "databaseName": "testDatabase"}
    #SQL_CreateNewUser.createNewUser(data["email"], data["userPass"], data["databaseName"])

    return jsonify({"Test": "OK"})

#POST /create new user
@app.route('/createUser', methods=['POST'])
def testPost():

    #Get data from POST request
    data = request.get_json()

    #Adds new user to database, and sets up new database for user
    SQL_CreateNewUser.createNewUser(data["email"], data["userPass"], data["databaseName"])

    print(data)

    #If POST request hhad no data,  return 400 error
    if not data:
        return jsonify({"Error": "No data"}), 400
    
    #Return data with 200 OK
    return jsonify(data)

# Run API
if __name__ == "__main__":
   app.run(debug=True, port=5001)