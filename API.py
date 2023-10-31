from flask import Flask, request
from flask_restx import Api, Resource, fields
import os

from functools import wraps
from flask import jsonify


from SQLConnections import SQL_CreateNewUser

print(os.getcwd())

'''
This will be automatically generated for each user and stored in a file
Only a variable for testing purposes
'''
API_KEY = 'TESTKEY' 

#Checks if API key is correct, if not returns error message
def require_api_key(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if request.headers.get('x-api-key') == API_KEY:
            return func(*args, **kwargs)
        else:
            return {"error": "API key missing or invalid"}, 401  # 401 = Unauthorized
    return decorated

#Api key authorization layout
authorizations = {
    'apiKey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'x-api-key'
    }
}

#defines app and api
app = Flask(__name__)

#defines api
api = Api(app,
          version='1.0',
          title='RapportSystem API Doc',
          description='Overview of the API endpoints',
          doc='/api/',
          authorizations=authorizations)

#defines namespace
ns = api.namespace('endpoints', description='API Endpoints')

#defines user model
user_model = api.model('User', {
    'email': fields.String(required=True, description='User email'),
    'userPass': fields.String(required=True, description='User password'),
    'databaseName': fields.String(required=True, description='Database name for the user')
})

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

#Post request for creating a new user & belonging database
@ns.route('/createUser')
class CreateUser(Resource):
    @api.doc('create_user')

    #requires API key to be used
    @api.doc(security='apiKey')
    #requires API key
    @require_api_key

    #expects user model from post request
    @api.expect(user_model, validate=True)
    def post(self):

        #Gets data from post request
        data = request.get_json()
        #Creates new user and database from data
        SQL_CreateNewUser.createNewUser(data["email"], data["userPass"], data["databaseName"])

        #returns error if no data is found or faulty
        if not data:
            return {"Error": "No data"}, 400
        return data

#Runs the API
if __name__ == "__main__":
    app.run(debug=True, port=5001)
