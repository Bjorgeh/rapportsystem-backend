from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_current_user
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
    @ns.route('/user/<int:user_id>')
    class Information(Resource):
        @ns.doc('userInfo',
                description='Info route, returns json with user information.',
                responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})

        #Requires valid jwt token
        @jwt_required()
        @vt.require_valid_token

        def get(self, user_id):
            # gets the current user
            current_user = get_jwt_identity()
            # connects to the database
            connection = SQLC.connector()
            # gets the user information
            user_info = SQLQ.get_user_info(connection, user_id)
            # closes the connection
            connection.close()

            # Extract the required fields from user_info
            user_info_json = {
                'user_Id': user_info['user_id'],
                'Name': user_info['username'],
                'email': user_info['email'],
                'user_accountType': user_info['user_accountType']
            }

            return jsonify(user_info_json), 200
