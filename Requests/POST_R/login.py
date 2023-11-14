from flask_restx import Resource
from flask import session, request,jsonify
#imports os
import os
current_directory = os.getcwd()
#imports sys
import sys
sys.path.append(os.path.join(current_directory))
from USER_session import sessionhandler as SH
from authorization import login_validation as login_auth
from Models import user_model as UM
#from SQLAdminConnections import SQL_AdminConnector as SQLC
#from SQLAdminConnections import SQL_AdminQuerys as SQLQ

#Login route
def login_route(ns):
    new_session = SH.UserSession(session)

    @ns.route('/login')
    class login(Resource):
        new_login_model = UM.login_model(ns)

        @ns.doc('login', description='Logs user in when given Username and Password...',
                responses={200: 'OK', 
                           400: 'Invalid Argument or faulty data', 
                           500: 'Internal server error'})
        
        #Validates input data
        @ns.expect(new_login_model, validate=True)
        def post(self):
            new_session.update_session()

            data = request.get_json()
            username = data["username"].lower()
            password = data["password"]

            login_validation = login_auth.loginValidation(username, password).validate_credentials()

            user_exists = login_validation[0]
            user_id = login_validation[1]
            user_accountType = login_validation[2]

            #checks if user exists
            if user_exists:
                
                # Setter nødvendige session-data
                session['user_id'] = user_id
                session['email'] = username
                session['account_type'] = user_accountType

                print(username, "created new session")

                #Removes old session and creates new 
                new_session.login()  

                #dict with current user
                current_user = {
                    "user_id": session['user_id'],
                    "email": session['email'],
                    "accountType": session['account_type']
                }
                return {"message": "Log-in successful", "Logged in as": current_user}, 200

            return{"Error": "Invalid username or password"}, 400
        
