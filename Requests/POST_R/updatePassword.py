#Imports nessesary modules
from flask_restx import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

#imports os
import os
current_directory = os.getcwd()
#imports sys
import sys
sys.path.append(os.path.join(current_directory))

#imports custom modules
from SQLAdminConnections import SQL_AdminConnector as SQLC
from SQLAdminConnections import SQL_AdminQuerys as SQLQ
from PW_hashHandler import pw_manager as hash
from Models import user_model as UM
from Common.Requirements import valid_token as vt
from USER_session import tokenHandler as TH

# Update password route
def update_password_route(ns):
    @ns.route('/updatePassword')
    class UpdatePassword(Resource):
        new_password_model = UM.update_password_model(ns)
        
        #Documentation for swagger UI
        @ns.doc('/updatePassword',
                description='Updates a users password when given new password and a exact duplicate of the new password.\n\nRequires valid JWT token authentication.',
                responses={
                    200: 'OK',
                    400: 'Invalid Argument or faulty data',
                    500: 'Internal server error'
                })
        
        #Validates input
        @ns.expect(new_password_model, validate=True)

        #Requires valid JWT token authentication
        @jwt_required()  
        @vt.require_valid_token

        #recives password data from user
        def post(self):
            current_user = get_jwt_identity()
            data = request.get_json()

            new_pass1 = data['password1']
            new_pass2 = data['password2']

            if not data:
                return {"Error": "No data provided"}
            
            #updates password
            return updatePassword(current_user['user_id'], current_user['email'], new_pass1, new_pass2)

#Function for updating password
def updatePassword(user_id, email, new_password1, new_password2):
    if not new_password1 == new_password2:
        return {"Password": "Does not match."}, 400

    #hashes password
    hashed_password = hash.hash(new_password1)
    
    #Connects to the database and updates the password
    connection = SQLC.SQLConAdmin()
    connection.connect()
    connection.execute_query(SQLQ.SQLQueries.use_users_database())
    connection.execute_query(SQLQ.SQLQueries.update_user_login_password(user_id, hashed_password))
    connection.execute_query(SQLQ.SQLQueries.update_sql_user_password(email, new_password1))
    connection.execute_query(SQLQ.SQLQueries.flush_privileges())
    connection.cnx.commit()
    connection.close()

        # Lager en instans av UserTokenHandler
    token_handler = TH.UserTokenHandler()

    # Logger ut brukeren
    token_handler.logout()

    return {"Password": "Updated!", "New password": "PROTECTED"}, 200