from flask_restx import Resource
from flask import jsonify
#imports os
import os
current_directory = os.getcwd()
#imports sys
import sys
sys.path.append(os.path.join(current_directory))

#imports requirements
from Common.Requirements.session_req import require_session
from Common.Requirements.admin_req import require_admin_account

#creates test route for admin account
def test_admin_route(ns):
    @ns.route('/test_admin')
    class Test(Resource):
        @ns.doc('test_admin',
                description='Test route, returns OK if the API is running and the user is logged in as Admin.',
                responses={200: 'OK', 
                           400: 'Invalid Argument', 
                           500: 'Mapping Key Error'})

        #requirements
        @require_session
        @require_admin_account  
        def get(self):
            return {"Test": "OK"},200