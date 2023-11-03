#imports flask & flask_restx for creating API
from flask import Flask, request, url_for, jsonify
from flask_restx import Api, Resource, fields
from flask_session import Session
#import datetime
import datetime
#imports os for getting current working directory
import os
#Imports function for requiring API key
from functools import wraps
#imports authorization file
from authorization import apiKeyAuth as auth
from authorization import session_config as SessionCFG

#imports fnction for creating new user and database
#from SQLAdminConnections import SQL_CreateNewLeaderUser
#from SQLAdminConnections import SQL_CreateNewOperatorUser

#imports function for requiring API key
from authorization import api_key as key
#imports user models
from Models.user_model import *
#PasswordHandler
from PW_hashHandler import pw_manager as hash
#imports user object
from USER_obj import users as USR
from USER_obj import new_user as makeUSR

#print(os.getcwd()) #uncomment for troubleshooting to see current working directory

#defines app and api
app = Flask(__name__)

app.config.from_object(SessionCFG)

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

#Post request for creating a new leader user & belonging database
@ns.route('/login')
class login(Resource):
    @api.doc('login')

    #expects user model from post request
    @api.expect(new_login_model, validate=True)
    def post(self):

        #Gets data from post request
        data = request.get_json()

        #Gets username and password from data
        username = data["username"]
        password = data["password"]

        '''
        Her skal sjekkes om bruker eksisterer i databasen og om passord er riktig.
        Hvis bruker eksisterer og passord er korrekt, skal det opprettes et user objekt - Her kan man også sjekke session osv.
        '''

        #Change print with password check
        print(username, password)

        #returns error if no data is found or faulty
        if not data:
            return {"Error": "No data"}, 400
        return data

#Get request for testing API connection
@ns.route('/test')
class Test(Resource):
    @api.doc('get_test')

    def get(self):
        #returns test data
        return {"Test": "OK"}

#Post request for creating a new leader user & belonging database
@ns.route('/createUser')
class CreateLeaderUser(Resource):
    @api.doc('create_user')

    #expects user model from post request
    @api.expect(new_user_model, validate=True)
    def post(self):

        #Gets data from post request
        data = request.get_json()

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