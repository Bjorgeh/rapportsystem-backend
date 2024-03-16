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
from flask_jwt_extended import get_jwt_identity
from Models import user_model as UM
from Common.Requirements import valid_token as vt
from Requests.dataHandler import dataInsertor as dataIns

# create Disa route
def insert_data(ns):
    @ns.route('/insertData')

    class insert_data_class(Resource):
        new_data_model = UM.insert_data_model(ns)
        
        #Documentation for swagger UI
        @ns.doc('/insertData',
                description='Takes data -> sets it to given table.\nNote: Date, Time and ID is automatically set by the system, and should not be provided.\nGet the table description from /api/user/get/rapportInfo to see what data is required.',
                responses={
                    200: 'OK',
                    400: 'Invalid Argument or faulty data',
                    500: 'Internal server error'
                })
        
        #Validates input
        @ns.expect(new_data_model, validate=True)

        #Requires valid JWT token authentication 
        @jwt_required()  
        @vt.require_valid_token

        #recives password data from user
        def post(self):
            data = request.get_json()
            current_user = get_jwt_identity()

            # get the table name and data from the request
            table_name = data['table_name']
            main_data = data['data']

            # check if forbidden keys are present in the data
            if any(key in main_data for key in ['date', 'time', 'id', 'sum_price', 'total_weight_melt', 'sum_kwh_used']):
                return {"Error": "Date, Time, ID, and columns with generated values should not be provided."}

            print("NOW: " + current_user["email"] + " is trying to insert data into table: " + table_name + " with data: " + str(main_data))

            # check if the main_data is empty
            if not main_data:
                return {"Error": "No data provided"}
            
            # return the result of the insertData function
            return {"Message":dataIns.Data_insertor(table_name, main_data).insertData()}
                