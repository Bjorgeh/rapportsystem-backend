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
from Requests.CreateRapport import RapportMaker as RM

# create Disa route
def createRapport(ns):
    @ns.route('/createRapport')

    class createDisaRapport(Resource):
        new_rapport_model = UM.create_rapport_model(ns)
        
        #Documentation for swagger UI
        @ns.doc('/createRapport',
                description='Creates a new rapport for user.',
                responses={
                    200: 'OK',
                    400: 'Invalid Argument or faulty data',
                    500: 'Internal server error'
                })
        
        #Validates input
        @ns.expect(new_rapport_model, validate=True)

        #Requires valid JWT token authentication & admin account
        @jwt_required()  
        @vt.require_valid_token
        @require_admin_account

        #recives password data from user
        def post(self):
            current_user = get_jwt_identity()
            data = request.get_json()

            #gets rapport type from userinput
            rapportType = data['rapportType']

            #checks if data is provided
            if not data:
                return {"Error": "No data provided"}
            
            #creates new rapport and returns status code
            return RM.RapportMaker().createRapport(current_user['user_id'], rapportType)
        