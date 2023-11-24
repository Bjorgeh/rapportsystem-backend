from flask_restx import Resource
from flask import jsonify, session
#imports os
import os
current_directory = os.getcwd()
#imports sys
import sys
sys.path.append(os.path.join(current_directory))
from flask_jwt_extended import jwt_required

def test_route(ns):
    @ns.route('/test')
    class Test(Resource):
        @ns.doc('test',
                description='Test route, returns OK if the API is running and the user is logged in.',
                responses={200: 'OK', 
                           400: 'Invalid Argument', 
                           500: 'Mapping Key Error'})
        
        #Requires JWT token
        @jwt_required()

        def get(self):
            return jsonify({"Test": "OK"})