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
from SQLAdminConnections import SQL_AdminConnector as SQLC
from SQLAdminConnections import SQL_AdminQuerys as SQLQ
from Common.Requirements.session_req import require_session

#Login route
def delete_user_route(ns):
    current_session = SH.UserSession(session)

    @ns.route('/deleteUser')
    class delete_user(Resource):
        deletion_model = UM.delete_model(ns)

        @ns.doc('Delete user', description='Deletes user when given Username and Password...',
                responses={200: 'OK', 
                           400: 'Invalid Argument or faulty data', 
                           500: 'Internal server error'})
        
        #Validates input data
        @ns.expect(deletion_model, validate=True)

        #requires valid session
        @require_session

        def post(self):

            data = request.get_json()
            username = data["username"].lower()
            password = data["password"]

            login_validation = login_auth.loginValidation(username, password).validate_credentials()

            user_exists = login_validation[0]

            #checks if user exists
            if user_exists:
                
                print(username, "Deleted user")

                #Removes session
                current_session.logout()

                #Removes user from database
                current_session.logout()
                remove_SQL_account(username)
                remove_user_account(username)
                remove_database(username)

                return {"message": "Removed account from database.", "We'll miss you": username}, 200

            return{"Error": "Invalid username or password"}, 400

#Function to remove user from database
def remove_SQL_account(username):
    try:
        connection = SQLC.SQLConAdmin()
        connection.connect()
        connection.execute_query(SQLQ.SQLQueries.delete_sql_user(username))
        connection.cnx.commit()

    except Exception as e:
        print(f"An error occurred during deletion: {e}")
        return False
    finally:
        if connection:
            connection.close()

#Removes user from user_info
def remove_user_account(username):
    try:
        connection = SQLC.SQLConAdmin()
        connection.connect()
        connection.execute_query(SQLQ.SQLQueries.use_users_database())
        connection.execute_query(SQLQ.SQLQueries.delete_user_from_user_info(username))
        connection.cnx.commit()

    except Exception as e:
        print(f"An error occurred during deletion: {e}")
        return False
    finally:
        if connection:
            connection.close()

#Removes users own database
def remove_database(username):
    try:
        connection = SQLC.SQLConAdmin()
        connection.connect()
        connection.execute_query(SQLQ.SQLQueries.drop_database(username))
        connection.cnx.commit()

    except Exception as e:
        print(f"An error occurred during deletion: {e}")
        return False
    finally:
        if connection:
            connection.close()