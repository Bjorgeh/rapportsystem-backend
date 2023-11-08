#imports flask & flask_restx for creating API
from flask import Flask, session
from flask_restx import Api
from flask_session import Session
#imports os
import os
current_directory = os.getcwd()
#imports sys
import sys
sys.path.append(os.path.join(current_directory))
#imports session handler
from USER_session import sessionhandler as SH
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

#defines namespace
ns_Post = api.namespace('POST', description='POST Endpoints')
ns_Get = api.namespace('GET', description='GET Endpoints')

#Sets up sessions
Session(app)
user_session = SH.UserSession(session, None)

#Gets the test route
get_test.test_route(ns_Get)

#Gets the test admin route
get_test_admin.test_admin_route(ns_Get)

#Gets the login route
post_login.login_route(ns_Post)

#Gets the logout route
get_logout.logout_route(ns_Get)

#Gets the create user route
post_createUser.create_user(ns_Post)

#Gets the update password route
post_updatePassword.update_password_route(ns_Post)
    
#Runs the APP/API
if __name__ == "__main__":
    app.run(debug=True, port=5001)