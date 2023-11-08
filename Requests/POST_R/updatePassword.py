from flask_restx import Resource
from flask import request
#imports os
import os
current_directory = os.getcwd()
#imports sys
import sys
sys.path.append(os.path.join(current_directory))

from USER_obj.users import logged_in_user
from Models import user_model as UM
from Common.Requirements.session_req import require_session

#Update password route
def update_password_route(ns):
    @ns.route('/updatePassword')
    class UpdatePassword(Resource):
        new_password_model = UM.update_password_model(ns)
        @ns.doc('/updatePassword')
        @ns.expect(new_password_model, validate=True)

        #requires valid session
        @require_session

        def post(self):
            #Gets data from post request
            data = request.get_json()

            #updates user password
            new_pass1 = data['password1']
            new_pass2 = data['password2']

            #returns error if no data is found or faulty
            if not data:
                return {"Error": "No data provided"}, 400
            
            return logged_in_user.updatePassword(new_pass1, new_pass2), 200