

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

#creates test route for admin account
def extract_data_from_database(ns):
    @ns.route('/extract_data')
    class Test(Resource):
        @ns.doc('extract_data',
                description='Data extraction route, returns all data the current user has access to from database.',
                responses={200: 'OK', 
                           400: 'Invalid Argument', 
                           500: 'Mapping Key Error'})

        #requirement for admin account & requires valid jwt token
        @jwt_required()
        @vt.require_valid_token
        @require_admin_account 
        
        def get(self):


            #returns data to user
            return {"Data": "OK"},200