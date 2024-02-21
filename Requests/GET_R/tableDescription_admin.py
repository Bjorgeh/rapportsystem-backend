

#import flask_restx
from flask_restx import Resource
#imports os
import os
current_directory = os.getcwd()
#imports sys - for pathing to files
import sys
sys.path.append(os.path.join(current_directory))

#imports requirements
from Common.Requirements.admin_req import require_admin_account
from Common.Requirements import valid_token as vt
from flask_jwt_extended import jwt_required, get_jwt_identity
#imports dataExtractor
from Requests.dataHandler import dataExtractor as dataEx

#creates test route for admin account
def extract_table_description_from_database(ns):
    @ns.route('/extract_tables')
    class Test(Resource):
        @ns.doc('extract_tables',
                description='Data extraction route, returns info about all tables a user has.',
                responses={200: 'OK', 
                           400: 'Invalid Argument', 
                           500: 'Mapping Key Error'})

        #requirement for admin account & requires valid jwt token
        @jwt_required()
        @vt.require_valid_token
        @require_admin_account 
        
        def get(self):
            current_user = get_jwt_identity()

            #creates dataExtractor object
            dataExtracor = dataEx.data_extractor()

            #returns data to user
            return {"Table_descriptions": dataExtracor.extractTableDescription(current_user['email'])},200