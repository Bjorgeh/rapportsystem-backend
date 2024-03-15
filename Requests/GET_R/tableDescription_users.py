

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
from flask_jwt_extended import jwt_required
#imports dataExtractor
from Requests.dataHandler import tableInfoExtractor as dataEx

#creates table description route for users
def extract_table_description(ns):
    @ns.route('/rapportInfo')
    class extract(Resource):
        @ns.doc('rapportInfo',
                description='Data extraction route, returns info about all rapports a user has.',
                responses={200: 'OK', 
                           400: 'Invalid Argument', 
                           500: 'Mapping Key Error'})

        #requirement for valid jwt token
        @jwt_required()
        @vt.require_valid_token

        def get(self):
            #creates dataExtractor object
            dataExtracor = dataEx.table_info_extractor()

            #returns data to user
            return {"Table_descriptions": dataExtracor.extractTableDescription()},200