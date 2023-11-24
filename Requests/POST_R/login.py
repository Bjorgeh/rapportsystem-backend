from flask_restx import Resource
from flask import request, jsonify
from mysql.connector import Error
import httpagentparser as parser
from flask_jwt_extended import create_access_token
import os
import sys

current_directory = os.getcwd()
sys.path.append(os.path.join(current_directory))

# Importer nødvendige moduler og klasser
from authorization import login_validation as login_auth
from Models import user_model as UM
from SQLAdminConnections import SQL_AdminConnector as SQLC
from SQLAdminConnections import SQL_AdminQuerys as SQLQ

# Login route
def login_route(ns):
    @ns.route('/login')
    class login(Resource):
        #Sets model for swagger
        new_login_model = UM.login_model(ns)
        @ns.doc('login', description='Logs user in when given Username and Password...',
                responses={200: 'OK', 
                           400: 'Invalid Argument or faulty data', 
                           500: 'Internal server error'})
        
        @ns.expect(new_login_model, validate=True)
        def post(self):
            data = request.get_json()
            username = data["username"].lower()
            password = data["password"]

            login_validation = login_auth.loginValidation(username, password).validate_credentials()
            user_exists, user_id, user_accountType = login_validation

            if user_exists:
                #Generates token for user
                access_token = create_access_token(identity={"user_id": user_id, "email": username, "accountType": user_accountType})

                #saved user activity to database
                save_activity(user_id)

                current_user = {
                    "user_id": user_id,
                    "email": username,
                    "accountType": user_accountType
                }
                #Returns token and user info
                return {"message": "Log-in successful", "Logged in as": current_user, "access_token": access_token}, 200
            #Returns error if user does not exist
            return {"Error": "Invalid username or password"}, 400

#Function for saving activity to database
def save_activity(user_id):

    #Checks if user has old activity - deletes 30 days old activity
    check_old_activity(user_id)

    #Gets ip address, browser name and operating system
    ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    parsed_agent = parser.detect(user_agent)
    browser_name = parsed_agent.get('browser', {}).get('name', 'Unknown')
    operating_system = parsed_agent.get('os', {}).get('name', 'Unknown')

    try:
        #connect to database
        connection = SQLC.SQLConAdmin()
        connection.connect()

        #Checking old activitys
        check_old_activity(user_id)

        connection.execute_query(SQLQ.SQLQueries.use_users_database())
        #save activity to database
        connection.execute_query(SQLQ.SQLQueries.insert_user_activity(user_id, ip_address, browser_name, operating_system))
        connection.cnx.commit()

    except Error as e:
        print("Error while saving activity to database.", e)
    finally:
        connection.close()

#Function for checking and deleting old activity
def check_old_activity(user_id):
    try:
        # Connect to the database
        connection = SQLC.SQLConAdmin()
        connection.connect()
        # Use the 'users' database
        connection.execute_query(SQLQ.SQLQueries.use_users_database())

        # Count the number of activities for the user
        result = connection.execute_query(SQLQ.SQLQueries.count_user_activities(user_id))
        activity_count = result[0][0] if result else 0

        # If there are more than 5 activities, fetch and delete the oldest one
        if activity_count > 4:
            result = connection.execute_query(SQLQ.SQLQueries.get_oldest_activity_id(user_id))
            oldest_activity_id = result[0][0] if result else None

            if oldest_activity_id:
                connection.execute_query(SQLQ.SQLQueries.delete_activity_by_id(oldest_activity_id))

        # Commit the changes
        connection.cnx.commit()

    except Error as e:
        print("Error while checking and deleting old activity.", e)
    finally:
        connection.close()


