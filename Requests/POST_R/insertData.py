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
from Common.Requirements.admin_req import require_admin_account
from Models import user_model as UM
from Common.Requirements import valid_token as vt
from Requests.dataHandler import dataInsertor as dataIns

# create Disa route
def insert_data(ns):
    @ns.route('/insertData')

    class isert_data_class(Resource):
        new_data_model = UM.insert_data_model(ns)
        
        #Documentation for swagger UI
        @ns.doc('/insertData',
                description='Takes data -> sets it to given table.',
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
        @require_admin_account

        #recives password data from user
        def post(self):
            current_user = get_jwt_identity()
            data = request.get_json()

            #gets rapport type from userinput
            table_name = data['table_name']
            main_data = data['data']

            #checks if data is provided
            if not data:
                return {"Error": "No data provided"}
            
            #creates new rapport and returns status code
            return {"Message":dataIns.Data_insertor().insertData(current_user['email'], table_name, main_data)}
        