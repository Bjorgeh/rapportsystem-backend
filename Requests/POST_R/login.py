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
from Models import user_model as UM

#Login route
def login_route(ns):
    new_session = SH.UserSession(session)
    #Post request for login
    @ns.route('/login')
    class login(Resource):
        new_login_model = UM.login_model(ns)
        @ns.doc('login')
        @ns.expect(new_login_model, validate=True)
        def post(self):

            # Checks if user is already logged in
            if 'user_id' in session:
                new_session.update_session()
                return {"Error": "Already logged in"}, 401
            
            data = request.get_json()
            username = data["username"].lower()
            password = data["password"]

            # Checks if username and password is ok
            login_validation = login_auth.loginValidation(username, password).validate_credentials()

            # Variabler fra login_validation
            user_exists = login_validation[0]
            user_id = login_validation[1]
            user_accountType = login_validation[2]

            # creates new session for logged in user.
            if user_exists:
                # Lager ny session
                session['user_id'] = user_id
                session['email'] = username
                session['account_type'] = user_accountType
                # Her kan du sette inn flere detaljer i session om nødvendig

                print(username, "created new session")

                # Creates current user dict for returning data
                current_user = {
                    "user_id": session['user_id'],
                    "email": session['email'],
                    "accountType": session['account_type']
                }

                new_session.login()

                # Returns success if username and password is ok
                return {"message": "Log-in successful", "Logged in as": current_user}, 200

            # Returns error if username or password is wrong
            return {"Error": "Invalid username or password"}, 401