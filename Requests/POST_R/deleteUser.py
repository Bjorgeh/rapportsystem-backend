from flask_restx import Resource
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import sys

current_directory = os.getcwd()
sys.path.append(os.path.join(current_directory))

from authorization import login_validation as login_auth
from Models import user_model as UM
from SQLAdminConnections import SQL_AdminConnector as SQLC
from SQLAdminConnections import SQL_AdminQuerys as SQLQ
from USER_session import tokenHandler as TH
from Common.Requirements import valid_token as vt

#Route for deleting user
def delete_user_route(ns):
    tokenHandler = TH.UserTokenHandler()

    @ns.route('/deleteUser')
    class delete_user(Resource):
        deletion_model = UM.delete_model(ns)

        #Documentation for swagger UI
        @ns.doc('Delete user', description='Deletes user when given Username and Password...',
                responses={200: 'OK', 400: 'Invalid Argument or faulty data', 500: 'Internal server error'})
        @ns.expect(deletion_model, validate=True)

        #Requires valid jwt token
        @jwt_required()
        @vt.require_valid_token

        #Function for deleting user
        def post(self):
            current_user = get_jwt_identity()
            data = request.get_json()
            username = data["username"].lower()
            password = data["password"]

            #checks if the user is trying to delete their own account
            if current_user['email'] != username:
                return {"Error": "Unauthorized deletion attempt"}, 403

            
            login_validation = login_auth.loginValidation(username, password).validate_credentials()
            user_exists = login_validation[0]

            #checks if the user exists
            if user_exists:
                print(username, "Deleted user")

                #logs user out and revokes token
                tokenHandler.logout()

                #Removes user from database
                remove_SQL_account(username)
                remove_user_account(username)
                remove_database(username)

                return {"message": "Removed account from database.", "We'll miss you": username}, 200
            return {"Error": "Invalid username or password"}, 400
        
#Function to remove user from database
def remove_SQL_account(username):
    try:
        connection = SQLC.SQLConAdmin()
        connection.connect()
        connection.execute_query(SQLQ.SQLQueries.use_users_database())
        connection.execute_query(SQLQ.SQLQueries.delete_sql_user(username))
        connection.cnx.commit()
    except Exception as e:
        print(f"An error occurred during deletion: {e}")
        return False
    finally:
        if connection:
            connection.close()

#Function to remove user from user_info table
def remove_user_account(username):
    try:
        user_id = get_user_id(username)
        if user_id:
            delete_user_tokens(user_id)
        connection = SQLC.SQLConAdmin()
        connection.connect()
        connection.execute_query(SQLQ.SQLQueries.use_users_database())
        connection.execute_query(SQLQ.SQLQueries.delete_activities_by_user_id(user_id))
        connection.execute_query(SQLQ.SQLQueries.delete_user_from_user_info(username))
        connection.cnx.commit()
    except Exception as e:
        print(f"An error occurred during user deletion: {e}")
    finally:
        if connection:
            connection.close()

#Removes users own database
def remove_database(username):
    try:
        connection = SQLC.SQLConAdmin()
        connection.connect()
        connection.execute_query(SQLQ.SQLQueries.use_users_database())
        connection.execute_query(SQLQ.SQLQueries.drop_database(username))
        connection.cnx.commit()
    except Exception as e:
        print(f"An error occurred during deletion: {e}")
        return False
    finally:
        if connection:
            connection.close()


#Function for getting user ID
def get_user_id(email):
    try:
        connection = SQLC.SQLConAdmin()
        connection.connect()
        connection.execute_query(SQLQ.SQLQueries.use_users_database())
        result = connection.execute_query(SQLQ.SQLQueries.get_user_id_by_email(email))
        if result:
            return result[0][0]  #return the first result
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if connection:
            connection.close()
    return None

#function for deleting user tokens by user ID
def delete_user_tokens(user_id):
    try:
        connection = SQLC.SQLConAdmin()
        connection.connect()
        connection.execute_query(SQLQ.SQLQueries.use_users_database())
        connection.execute_query(SQLQ.SQLQueries.delete_tokens_by_user_id(user_id))
        connection.cnx.commit()
    except Exception as e:
        print(f"An error occurred during token deletion: {e}")
    finally:
        if connection:
            connection.close()




