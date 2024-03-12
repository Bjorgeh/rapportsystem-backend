from flask_restx import Resource
from flask import request, jsonify

#imports os
import os
current_directory = os.getcwd()
#imports sys
import sys
sys.path.append(os.path.join(current_directory))
from PW_hashHandler import pw_manager as hash
from Models import user_model as UM
from USER_obj import new_sub_user as makeUSR
from Common.Requirements.admin_req import require_admin_account
from flask_jwt_extended import jwt_required, get_jwt_identity
from Common.Requirements import valid_token as vt

#Create subuser route
def create_sub_operator(ns):
    #Post request for creating a new leader user & belonging database
    @ns.route('/createSubOperator')
    class CreateLeaderUser(Resource):
        new_sub_user_model = UM.sub_operator_model(ns)
        @ns.doc('admin_create_sub_operator_user',
                description='Create new operator user when given Email, Password and rapport name',
                responses={
                    200: 'OK',
                    400: 'Invalid Argument or faulty data',
                    500: 'Internal server error'
                })

        #expects user model from post request
        @ns.expect(new_sub_user_model, validate=True)

        #Requires valid JWT token authentication 
        @jwt_required()  
        @vt.require_valid_token
        @require_admin_account

        def post(self):

            #Gets admins email from JWT token
            creatorID = get_jwt_identity()
            creatorAccount = creatorID['email']

            #Gets data from post request
            data = request.get_json()
            
            #Sets email and accountType from post request to loweer case
            email = str(data['email']).lower()
            rapportName = str(data['rapportName']).lower()
           
            #uses the new objekt to create new user in database
            makeUSR.createSubUser(email, hash.hash(data['password']), "operator", creatorAccount).saveToDB()
            #makeUSR.createSubUser(email, hash.hash(data['password']), accountType).saveToDB()

            #returns error if no data is found or faulty
            if not data:
                return {"Error": "No data"}, 400
            return data