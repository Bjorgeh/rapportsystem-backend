#Imports nessesary modules
from flask_restx import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

#imports os
import os
current_directory = os.getcwd()
#imports sys
import sys
sys.path.append(os.path.join(current_directory))

#imports custom modules
from Models import user_model as UM
from Common.Requirements import valid_token as vt
from Requests.dataHandler import dataExtractor as DE

# extract by date or count
def extract_by_date_or_count(ns):
    @ns.route('/extractPreciseData')

    class extractDateNum(Resource):
        data_date_num_model = UM.data_date_num_model(ns)
        
        #Documentation for swagger UI
        @ns.doc('/extractPreciseData',
                description='Takes in a data to extract precise data from the database based on date or number of rapports',
                responses={
                    200: 'OK',
                    400: 'Invalid Argument or faulty data',
                    500: 'Internal server error'
                })
        
        #Validates input
        @ns.expect(data_date_num_model, validate=True)

        #Requires valid JWT token authentication & admin account
        @jwt_required()  
        @vt.require_valid_token

        #recives password data from user
        def post(self):
            current_user = get_jwt_identity()
            data = request.get_json()

            table_name = data.get('table_name')

            date_start = data.get('date_start')

            date_stop = data.get('date_stop')

            rapport_count = data.get('rapport_count')

            #checks if data is provided
            if not data:
                return {"Error": "No data provided"}
            
            #creates new rapport and returns status code
            return DE.data_extractor().extractGivenTable(current_user['email'], table_name, date_start, date_stop,rapport_count)
        