#imports flask & flask_restx for creating API
from flask import Flask
from flask_restx import Api
from flask_session import Session
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
#Post-requests
from Requests.POST_R import login as post_login
from Requests.POST_R import createUser as post_createUser
from Requests.POST_R import updatePassword as post_updatePassword

#imports secret.py
from SQLConnections import secret as Secret

#defines app and api
app = Flask(__name__)

#Sets app config SECRET_KEY and SESSION_TYPE
Secret.setConfig(app)

#defines api
api = Api(app,
          version='1.0',
          title='RapportSystem API Doc',
          description='Overview of the API endpoints',
          doc='/api/'
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
Session(app)

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
#Create user route
post_createUser.create_user(user_post)

'''POST - api/user/post'''
#Login route
post_login.login_route(user_post)
#Update password route
post_updatePassword.update_password_route(user_post)


'''
  ----------------------------
 |                            |
 |   Routes for Admin users   |
 V                            V
'''

'''GET - api/admin/get'''

#Test admin route
get_test_admin.test_admin_route(admin_get)

'''POST - api/admin/post'''
#POST


'''
  --------------------------                       
 |                          |
 |    Routes for Leaders    |
 V                          V
'''

'''GET - api/leader/get'''
#GET

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

'''POST - api/operator/post'''
#POST


'''Runs the API'''
if __name__ == "__main__":
    #Hosts the API on port 5001 and sets debug to True
    app.run(host='0.0.0.0',debug=True, port=5001)