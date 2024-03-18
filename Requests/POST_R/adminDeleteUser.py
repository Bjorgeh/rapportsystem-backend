from flask_restx import Resource
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import sys

current_directory = os.getcwd()
sys.path.append(os.path.join(current_directory))

#Imports user model
from Models import user_model as UM
#Imports SQL admin connections
from SQLAdminConnections import SQL_AdminConnector as SQLC
from SQLAdminConnections import SQL_AdminQuerys as SQLQ
#Imports token handler
from USER_session import tokenHandler as TH
#Imports requirements
from Common.Requirements import valid_token as vt
from Common.Requirements.admin_req import require_admin_account

#Route for deleting user
def admin_delete_subuser_route(ns):
    tokenHandler = TH.UserTokenHandler()

    @ns.route('/deleteSubUser')
    class delete_subuser(Resource):
        deletion_model = UM.sub_delete_model(ns)

        #Documentation for swagger UI
        @ns.doc('Delete user', 
                description='Deletes subuser when given Username.',
                responses={200: 'OK', 
                           400: 'Invalid Argument or faulty data', 
                           500: 'Internal server error'})
        @ns.expect(deletion_model, validate=True)

        #Requires valid jwt token & admin account
        @jwt_required()
        @vt.require_valid_token
        @require_admin_account

        # post function for deleting user
        def post(self):
            data = request.get_json()
            username = data["username"].lower()

            #Removes user from database
            remove_SQL_account(username)
            remove_user_account(username)

            return {"message": "Removed.", "Goodbye": username}, 200
        
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




