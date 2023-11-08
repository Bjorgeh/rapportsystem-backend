from flask_restx import Resource
from flask import request, session
#imports os
import os
current_directory = os.getcwd()
#imports sys
import sys
sys.path.append(os.path.join(current_directory))
from PW_hashHandler import pw_manager as hash
from Models import user_model as UM
from USER_obj import new_user as makeUSR

#Create user route
def create_user(ns):
    #Post request for creating a new leader user & belonging database
    @ns.route('/createUser')
    class CreateLeaderUser(Resource):
        new_user_model = UM.user_model(ns)
        @ns.doc('create_user')

        #expects user model from post request
        @ns.expect(new_user_model, validate=True)
        def post(self):

            #Gets data from post request
            data = request.get_json()
            
            #Sets email and accountType from post request to loweer case
            email = str(data['email']).lower()
            accountType = str(data['accountType']).lower()
            print("New Account: ", email, "Type: ", accountType)

            #Makes new User Objekt
            #new_user = USR.users(None,email, hash.hash(data['password']), accountType,None,None)
           
            #uses the new objekt to create new user in database
            makeUSR.createUser(email, hash.hash(data['password']), accountType).saveToDB()

            #returns error if no data is found or faulty
            if not data:
                return {"Error": "No data"}, 400
            return data