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
from flask import jsonify

#defines activity route 
def uInfo_route(ns):
    @ns.route('/user/info')
    class Information(Resource):
        @ns.doc('userInfo',
                description='Info route, returns json with user information.',
                responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})

        #Requires valid jwt token
        @jwt_required()
        @vt.require_valid_token

        def get(self):
            # gets the current user
            current_user = get_jwt_identity()
            # connects to the database
            connection = SQLC.SQLConAdmin()
            connection.connect()
            connection.execute_query(SQLQ.SQLQueries.use_users_database())
            # gets the user information - From adminQuerry
            user_info = SQLQ.SQLQueries.get_user_information_by_id(current_user['user_id'])

            result = connection.execute_query(user_info)
            connection.cnx.commit()

            

            if result:
                for row in result:
                    #Format activity_timestamp as a string
                    created_timestamp = row[5].strftime('%Y-%m-%d %H:%M:%S') if row[5] else None
                    updated_timestamp = row[6].strftime('%Y-%m-%d %H:%M:%S') if row[6] else None

                    user_info = {
                        'user_Id': row[0],
                        'email': row[1],
                        'accountType': row[2],
                        'dbName': row[3],
                        'created_timestamp': created_timestamp,
                        'updater_timestamp': updated_timestamp

                    }
            

            
            # closes the connection
            connection.close()

            return user_info
