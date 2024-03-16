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
from Common.Requirements import leader_req as lr
from Requests.dataHandler import dataChanger as dataChanger

# create Disa route
def delete_last_row(ns):
    @ns.route('/deleteLastRapport')

    class delete_data_class(Resource):
        del_last_report_model = UM.remove_last_row(ns)
        
        #Documentation for swagger UI
        @ns.doc('/deleteLastRapport',
                description='Takes tablename -> Removes last added report.',
                responses={
                    200: 'OK',
                    400: 'Invalid Argument or faulty data',
                    500: 'Internal server error'
                })
        
        #Validates input
        @ns.expect(del_last_report_model, validate=True)

        #Requires valid JWT token authentication 
        @jwt_required()  
        @vt.require_valid_token
        @lr.require_leader_account
        

        #recives password data from user
        def post(self):
            data = request.get_json()
            current_user = get_jwt_identity()

            #gets data from request -> table & data
            table_name = data['table_name']
            print("NOW: " + current_user["email"] + " is trying to delete last row from: " + table_name )

            #checks if data is provided
            if not data:
                return {"Error": "No data provided"}
            
            #Returns the result of the insertData function & inserts data into database
            return {"Message":dataChanger.data_changer(table_name).deleteLastRow()}
        