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
def uInfo_route(ns):
    @ns.route('/info')
    class Information(Resource):
        @ns.doc('userInfo',
                description='Info route, returns json with user information.',
                responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})

        #Requires valid jwt token
        @jwt_required()
        @vt.require_valid_token

        def get(self):
            current_user = get_jwt_identity()
            return {"User_info": fetch_user_info(current_user['user_id'])}

#fetches the last 5 activities from the database
def fetch_user_info(user_id):
    
    try:
        #Connect to the database
        connection = SQLC.SQLConAdmin()
        connection.connect()
        connection.execute_query(SQLQ.SQLQueries.use_users_database())


        result = connection.execute_query(SQLQ.SQLQueries.get_user_information_by_id(user_id))
        
        #If the result is not empty
        if result:
            for row in result:

                formatted_timestamp = row[5].strftime('%Y-%m-%d %H:%M:%S') if row[5] else None

                #Return the result  as a dictionary
                user_information = {
                    "id": row[0],
                    "email": row[1],
                    "userPass": row[2],
                    "accountType": row[3],
                    "databaseName": row[4],
                    "activity_timestamp": formatted_timestamp
                }
                
                
                    
    except Error as e:
        print("Error while fetching activities.", e)
    finally:
        connection.close()

    return user_information

        
