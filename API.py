#imports flask & flask_restx for creating API
from flask import Flask, request
from flask_restx import Api, Resource, fields
#imports os for getting current working directory
import os
#Imports function for requiring API key
from functools import wraps
from flask import jsonify
#imports authorization file
from authorization import apiKeyAuth as auth
#imports fnction for creating new user and database
from SQLAdminConnections import SQL_CreateNewLeaderUser
from SQLAdminConnections import SQL_CreateNewOperatorUser
#imports function for requiring API key
from authorization import api_key as key
#imports user models
from Models.user_model import *
from PW_hashHandler import pw_manager as hash

#print(os.getcwd()) #uncomment for troubleshooting to see current working directory

#Checks if API key is correct, if not returns error message
def require_api_key(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if request.headers.get('x-api-key') == key.getAPIKey():
            return func(*args, **kwargs)
        else:
            return {"error": "API key missing or invalid"}, 401  # 401 = Unauthorized
    return decorated

#Gets api key settings from authorization file
ApiKey_settings = auth.API_KEY_SETTINGS

#defines app and api
app = Flask(__name__)

#defines api
api = Api(app,
          version='1.0',
          title='RapportSystem API Doc',
          description='Overview of the API endpoints',
          doc='/api/',
          authorizations=ApiKey_settings)

#gets user models
new_leader_user_model = leader_user_model(api)
new_operator_user_model = operator_user_model(api)

#defines namespace
ns = api.namespace('endpoints', description='API Endpoints')

#Get request for testing API connection
@ns.route('/test')
class Test(Resource):
    @api.doc('get_test')

    #requires API key to be used
    @api.doc(security='apiKey')
    #requires API key
    @require_api_key

    def get(self):
        '''Fetch a test data'''
        return {"Test": "OK"}

#Post request for creating a new leader user & belonging database
@ns.route('/createLeaderUser')
class CreateLeaderUser(Resource):
    @api.doc('create_leader_user')

    #requires API key to be used
    @api.doc(security='apiKey')
    #requires API key
    @require_api_key

    #expects user model from post request
    @api.expect(new_leader_user_model, validate=True)
    def post(self):

        #Gets data from post request
        data = request.get_json()

        #Creates new user and database from data
        SQL_CreateNewLeaderUser.createNewLeaderUser(data["email"], hash.hash(data['userPass']), data["databaseName"])

        #returns error if no data is found or faulty
        if not data:
            return {"Error": "No data"}, 400
        return data
    
#Post request for creating a new operator user
@ns.route('/createOperatorUser')
class CreateUser(Resource):
    @api.doc('create_leader_user')

    #requires API key to be used
    @api.doc(security='apiKey')
    #requires API key
    @require_api_key

    #expects user model from post request
    @api.expect(new_operator_user_model, validate=True)
    def post(self):

        #Gets data from post request
        data = request.get_json()
        #Creates new user from data
        SQL_CreateNewOperatorUser.createNewOperatorUser(data["email"], hash.hash(data['userPass']))

        #returns error if no data is found or faulty
        if not data:
            return {"Error": "No data"}, 400
        return data

#Runs the APP/API
if __name__ == "__main__":
    app.run(debug=True, port=5001)