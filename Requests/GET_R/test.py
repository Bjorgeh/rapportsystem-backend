from flask_restx import Resource
from flask import jsonify, session
#imports os
import os
current_directory = os.getcwd()
#imports sys
import sys
sys.path.append(os.path.join(current_directory))
from flask_jwt_extended import jwt_required
from Common.Requirements import valid_token as vt

#test route for all userstypes
def test_route(ns):
    @ns.route('/userStatus')
    class Test(Resource):
        @ns.doc('userStatus',
                description='Test route, returns OK if the API is running and the user is logged in.',
                responses={200: 'OK', 
                           400: 'Invalid Argument', 
                           500: 'Mapping Key Error'})
        
        #Requires valid jwt token
        @jwt_required()
        @vt.require_valid_token

        def get(self):
            return jsonify({"Status": "OK"})