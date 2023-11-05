#imports flask & flask_restx for creating API
from flask import Flask, request, url_for, jsonify,session
from flask_restx import Api, Resource, fields
from flask_session import Session
#import datetime
import datetime
#imports os for getting current working directory
import os
#Imports function for requiring API key
from functools import wraps
#imports authorization file
#from authorization import apiKeyAuth as auth

#imports function for requiring API key
from authorization import api_key as key
#imports user models
from Models.user_model import *
#PasswordHandler
from PW_hashHandler import pw_manager as hash
#imports user object
from USER_obj import users as USR
from USER_obj import new_user as makeUSR

from USER_session import sessionhandler as SH

#print(os.getcwd()) #uncomment for troubleshooting to see current working directory

#defines app and api
app = Flask(__name__)

app.config['SECRET_KEY'] = 'TESTKEY'
app.config['SESSION_TYPE'] = 'filesystem'

#defines api
api = Api(app,
          version='1.0',
          title='RapportSystem API Doc',
          description='Overview of the API endpoints',
          doc='/api/'
        )

#gets and implements user models
new_user_model = user_model(api)
new_login_model = login_model(api)

#defines namespace
ns = api.namespace('api', description='API Endpoints')

#Sets up sessions
Session(app)
user_session = SH.UserSession(session, None)

#Get request for testing API connection
@ns.route('/test')
class Test(Resource):
    @api.doc('get_test')

    def get(self):
        #returns test data
        return {"Test": "OK"}

#Post request for login
@ns.route('/login')
class login(Resource):
    @api.doc('login')

    @api.expect(new_login_model, validate=True)
    def post(self):
        data = request.get_json()

        ####################################
        username = data["username"]
        password = data["password"]

        #Skal endres til å sjekke mot database
        user_exists = True 
        user_id = "2"  
        ####################################

        #creates new session for logged in user.
        if user_exists:
            user_session.user_id = user_id
            user_session.login()

            print("User" + user_id + " logged in")

            #Her skal session lagres i database -- lage objekt av bruker som logger inn?

            return {"message": "Logged in successfully"}, 200

        return {"Error": "Invalid username or password"}, 401

#Get request for logout
@ns.route('/logout')
class logout(Resource):
    @api.doc('logout')

    def get(self):
        user_session = SH.UserSession(session, None)
        user_session.logout()
        
        return {"Logout": "OK"}, 200

#Post request for creating a new leader user & belonging database
@ns.route('/createUser')
class CreateLeaderUser(Resource):
    @api.doc('create_user')

    #expects user model from post request
    @api.expect(new_user_model, validate=True)
    def post(self):

        #Gets data from post request
        data = request.get_json()

        #accountType = data["accountType"].lower()

        #returns error if no account data is found
        #if accountType != "leader" or accountType != "operator":
        #    return {"Error": "Invalid account type"}, 400

        #Makes new User Objekt
        new_user = USR.users(data["email"], hash.hash(data['password']), data["accountType"])

        #Creates new user in database
        makeUSR.createUser(new_user).saveToDB()

        #returns error if no data is found or faulty
        if not data:
            return {"Error": "No data"}, 400
        return data

#Runs the APP/API
if __name__ == "__main__":
    app.run(debug=True, port=5001)