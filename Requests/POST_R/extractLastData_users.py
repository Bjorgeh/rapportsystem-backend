from flask_restx import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

#imports os
import os
current_directory = os.getcwd()
#imports sys - for pathing to files
import sys
sys.path.append(os.path.join(current_directory))
#Imports user model
from Models import user_model as UM
#imports requirements
from Common.Requirements.leader_req import require_leader_account
from Common.Requirements import valid_token as vt
from flask_jwt_extended import jwt_required, get_jwt_identity
#imports dataExtractor
from Requests.dataHandler import dataExtractor as dataEx

#extract last data from database
def extract_last_data_from_database(ns):
    @ns.route('/extract_last')
    class Test(Resource):
        last_data_model = UM.get_last_row(ns)
        @ns.doc('extract_last',
                description='Data extraction route, returns all data the current user has access to from database.',
                responses={200: 'OK', 
                           400: 'Invalid Argument', 
                           500: 'Mapping Key Error'})
        @ns.expect(last_data_model, validate=True)

        #requirement for leader account & requires valid jwt token
        @jwt_required()
        @vt.require_valid_token
        @require_leader_account
        
        def post(self):
            current_user = get_jwt_identity()
            data = request.get_json()

            table_name = data['table_name']

            dataExtracor = dataEx.data_extractor()

            #returns latest data to user
            return dataExtracor.extractLastData(current_user['email'],table_name),200