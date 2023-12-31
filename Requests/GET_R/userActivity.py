from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from mysql.connector import Error
#imports os
import os
current_directory = os.getcwd()
#imports sys
import sys
sys.path.append(os.path.join(current_directory))

from SQLAdminConnections import SQL_AdminConnector as SQLC
from SQLAdminConnections import SQL_AdminQuerys as SQLQ
from Common.Requirements import valid_token as vt

#defines activity route 
def activity_route(ns):
    @ns.route('/activity')
    class activity(Resource):
        @ns.doc('userActivity',
                description='Info route, returns json with 5 last IP and user agent logins.',
                responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})

        #Requires valid jwt token
        @jwt_required()
        @vt.require_valid_token

        def get(self):
            current_user = get_jwt_identity()
            return {"Activity": fetch_oldest_activities(current_user['user_id'])}

#fetches the last 5 activities from the database
def fetch_oldest_activities(user_id):
    activities = []
    try:
        #Connect to the database
        connection = SQLC.SQLConAdmin()
        connection.connect()
        connection.execute_query(SQLQ.SQLQueries.use_users_database())
        #Get the result from the query - 5 or fewer activities
        result = connection.execute_query(SQLQ.SQLQueries.get_oldest_activities(user_id))
        
        #If the result is not empty
        if result:
            for row in result:
                
                #Format activity_timestamp as a string
                formatted_timestamp = row[5].strftime('%Y-%m-%d %H:%M:%S') if row[5] else None

                #Create a dictionary of the result
                activity = {
                    'id': row[0],
                    'user_id': row[1],
                    'ip_address': row[2],
                    'user_agent': row[3],
                    'operating_system': row[4],
                    'activity_timestamp': formatted_timestamp
                }
                activities.append(activity)
                    
    except Error as e:
        print("Error while fetching activities.", e)
    finally:
        connection.close()

    return activities

        
