#imports flask & flask_restx for creating API
from flask import Flask #,session
from flask_restx import Api
#from flask_session import Session
from flask_cors import CORS
#Imports datetime for cookie expiration
from datetime import timedelta
#imports os
import os
current_directory = os.getcwd()
#imports sys
import sys
sys.path.append(os.path.join(current_directory))
#Get-requests
from Requests.GET_R import test as get_test
from Requests.GET_R import test_admin as get_test_admin
from Requests.GET_R import logout as get_logout
from Requests.GET_R import userActivity as get_userActivity
from Requests.GET_R import userInfo as get_userInfo
from Requests.GET_R import extractData_admin as extract_data_from_database
from Requests.GET_R import tableDescription_admin as extract_table_description_from_database
from Requests.GET_R import test_leader as get_test_leader
from Requests.GET_R import test_operator as get_test_operator
#Post-requests
from Requests.POST_R import login as post_login
from Requests.POST_R import createUser as post_createUser
from Requests.POST_R import updatePassword as post_updatePassword
from Requests.POST_R import deleteUser as post_deleteUser
from Requests.POST_R import createRapport as post_createRapport
from Requests.POST_R import insertData_admin as post_insertData
from Requests.POST_R import adminCreateSubLeader as post_createLeaderSubUser
from Requests.POST_R import adminCreateSubOperator as post_createOperatorSubUser

#imports secret.py
from SQLConnections import secret as Secret

#For API
from flask_jwt_extended import JWTManager
#for login route
from flask_jwt_extended import create_access_token
#for protected routes
from flask_jwt_extended import jwt_required

#defines app and api
app = Flask(__name__)

#Sets app config SECRET_KEY and SESSION_TYPE
Secret.setConfig(app)

#sets up JWT - this shall be moved to the secret file
JWTManager(app)

#Sets up CORS
CORS(app,supports_credentials=True)

#Set up authorizations for swagger - Usage: Bearer <access_token> - This is not acutal an API key, but a token. functions as a key.
authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Type in the *Bearer* space token'
    },
}

#defines api
api = Api(app,
          version='1.0',
          title='RapportSystem API Doc',
          description='Overview of the API endpoints.\n\nUsage:\n- Log in\n- Go to authorize\n- Type in the *Bearer* space access_token\n- Use the API',
          doc='/api/',
          authorizations=authorizations, 
          security='Bearer Auth'
        )

'''Defines namespaces'''
#defines namespace all users.
user_post = api.namespace('api/user/post', description='POST Endpoints')
user_get = api.namespace('api/user/get', description='GET Endpoints')
#defines namespace for admin users.
admin_post = api.namespace('api/admin/post', description='POST Endpoints')
admin_get = api.namespace('api/admin/get', description='GET Endpoints')
#defines namespace for leader users.
leader_post = api.namespace('api/leader/post', description='POST Endpoints')
leader_get = api.namespace('api/leader/get', description='GET Endpoints')
#defines namespace for operator users.
operator_post = api.namespace('api/operator/post', description='POST Endpoints')
operator_get = api.namespace('api/operator/get', description='GET Endpoints')

#Sets up sessions
#Session(app)

#Routes for the API
'''
  ------------------------
|                         |
|   Routes for all users  |
V                         V
'''

'''GET - api/user/get'''

#Test route
get_test.test_route(user_get)
#Logout route
get_logout.logout_route(user_get)
#Get user activity
get_userActivity.activity_route(user_get)
#Get user information
get_userInfo.uInfo_route(user_get)

'''POST - api/user/post'''
#Login route
post_login.login_route(user_post)
#Update password route
post_updatePassword.update_password_route(user_post)
#Create user route
post_createUser.create_user(user_post)
#Delete user route
post_deleteUser.delete_user_route(user_post)


'''
  ----------------------------
 |                            |
 |   Routes for Admin users   |
 V                            V
'''

'''GET - api/admin/get'''
#Test admin route
get_test_admin.test_admin_route(admin_get)
#Extract data from database
extract_data_from_database.extract_data_from_database(admin_get)
#Extract table description from database
extract_table_description_from_database.extract_table_description_from_database(admin_get)

'''POST - api/admin/post'''
#Create Rapport route
post_createRapport.createRapport(admin_post)
#Insert data route
post_insertData.insert_data(admin_post)
#Create leader sub user route
post_createLeaderSubUser.create_sub_leader(admin_post)
#Create operator sub user route
post_createOperatorSubUser.create_sub_operator(admin_post)

'''
  --------------------------                       
 |                          |
 |    Routes for Leaders    |
 V                          V
'''

'''GET - api/leader/get'''
#GET
get_test_leader.test_leader_route(leader_get)
'''POST - api/leader/post'''
#POST


'''
  ---------------------------
 |                           |
 |    Routes for Operators   |
 V                           V
'''

'''GET - api/operator/get'''
#GET
get_test_operator.test_operator_route(operator_get)
'''POST - api/operator/post'''
#POST


'''
  ---------------------------
 |                           |
 |       RUNS the API        |
 V                           V
'''
if __name__ == "__main__":
    #Hosts the API on port 5001 and sets debug to True
    app.run(host='0.0.0.0',debug=True, port=5001)