#import flask_restx
from flask_restx import Resource
#imports os
import os
current_directory = os.getcwd()
#imports sys - for pathing to files
import sys
sys.path.append(os.path.join(current_directory))

#imports requirements
from Common.Requirements import valid_token as vt
from flask_jwt_extended import jwt_required, get_jwt_identity
from Common.Requirements.admin_req import require_admin_account
#imports dataExtractor
from Requests.dataHandler import dataExtractor as dataEx

#creates table description route for users
def extractSubUsers(ns):
    @ns.route('/extractSubUsers')
    class extract(Resource):
        @ns.doc('extractSubUsers',
                description='Data extraction route, returns info about all subusers a admin has.',
                responses={200: 'OK', 
                           400: 'Invalid Argument', 
                           500: 'Mapping Key Error'})

        #requirement for valid jwt token
        @jwt_required()
        @vt.require_valid_token
        @require_admin_account

        def get(self):
            #creates dataExtractor object
            dataExtracor = dataEx.data_extractor()
            current_user = get_jwt_identity()

            #returns data to user
            return {current_user['email']:dataExtracor.getAllSubUsers()},200