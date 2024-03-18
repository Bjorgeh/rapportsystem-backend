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
def admin_update_password_route(ns):
    @ns.route('/updateUsersPassword')
    class admin_UpdatePassword(Resource):
        new_password_model = UM.admin_update_password_model(ns)
        
        #Documentation for swagger UI
        @ns.doc('/updateUsersPassword',
                description='Updates a users password when given username, password and a exact duplicate of the new password.\n\nRequires valid adminaccount and JWT token.',
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

        #recives user and password from admin and updates the password
        def post(self):
            data = request.get_json()

            username = data['username']
            new_pass1 = data['password1']
            new_pass2 = data['password2']

            if not data:
                return {"Error": "No data provided"}
            
            #updates password
            return updatePassword(username, new_pass1, new_pass2)

#Function for updating password
def updatePassword(email, new_password1, new_password2):
    if not new_password1 == new_password2:
        return {"Password": "Does not match."}, 400

    #hashes password
    hashed_password = hash.hash(new_password1)
    
    #Connects to the database and updates the password
    connection = SQLC.SQLConAdmin()
    connection.connect()
    connection.execute_query(SQLQ.SQLQueries.use_users_database())

    #gets user id
    user_id = connection.execute_query(SQLQ.SQLQueries.get_user_id_by_email(email))
    if not user_id:
        return {"Error": "User not found."}, 400
    user_id = user_id[0][0]

    #updates password
    connection.execute_query(SQLQ.SQLQueries.update_user_login_password(user_id, hashed_password))
    connection.execute_query(SQLQ.SQLQueries.update_sql_user_password(email, new_password1))
    connection.execute_query(SQLQ.SQLQueries.flush_privileges())
    connection.cnx.commit()
    connection.close()

        # Lager en instans av UserTokenHandler
    token_handler = TH.UserTokenHandler()

    # Logger ut brukeren
    token_handler.logout()

    return {"User": email, "Password": "Updated"}, 200