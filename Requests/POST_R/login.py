from flask_restx import Resource
from flask import session, request
#imports os
import os
current_directory = os.getcwd()
#imports sys
import sys
sys.path.append(os.path.join(current_directory))

from USER_session import sessionhandler as SH
from authorization import login_validation as login_auth
from USER_obj.users import logged_in_user
from Models import user_model as UM

user_session = SH.UserSession(session, None)

#Login route
def login_route(ns):
    #Post request for login
    @ns.route('/login')
    class login(Resource):
        new_login_model = UM.login_model(ns)
        @ns.doc('login')

        @ns.expect(new_login_model, validate=True)
        def post(self):

            #Checks if user is already logged in
            if user_session.is_authenticated():
                return {"Error": "Already logged in"}, 401
            
            #user_session = SH.UserSession(session, None)
            data = request.get_json()
            #Sets username and password from post request
            username = data["username"]
            #Sets username to lower case
            if isinstance(username, str):
                username = data['username'].lower()
            password = data["password"]

            #Checks if username and password is ok
            login_validation = login_auth.loginValidation(username, password).validate_credentials()

            #Variabler fra login_validation
            user_exists = login_validation[0]
            user_id = login_validation[1]
            user_accountType = login_validation[2]

            #creates new session for logged in user.
            if user_exists:
                user_session.user_id = user_id

                #Lager ny session
                user_session.login()
                print(username, "created new session")

                #Updates userobject with new data
                logged_in_user.updateID(user_id)
                logged_in_user.updateEmail(username)
                logged_in_user.updateAccountType(user_accountType)
                logged_in_user.updatesessionId(user_session.get_session_id())
                logged_in_user.updateDatabaseName(None)
                #logged_in_user.updatePassword(None)

                #Creates current user dict for returning data
                current_user = {
                    "user_id": logged_in_user.getID(),
                    "email": logged_in_user.getEmail(),
                    "password": logged_in_user.getPassword(),
                    "accountType": logged_in_user.getAccountType(),
                    "databaseName": logged_in_user.getDatabaseName(),
                    "session_id": logged_in_user.getSessionID()
                }

                #Returns success if username and password is ok
                return {"message": "Log-in successfull", "Logged in as": current_user}, 200
            #Returns error if username or password is wrong
            return {"Error": "Invalid username or password"}, 401