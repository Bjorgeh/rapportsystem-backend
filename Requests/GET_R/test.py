from flask_restx import Resource
from flask import jsonify
#imports os
import os
current_directory = os.getcwd()
#imports sys
import sys
sys.path.append(os.path.join(current_directory))

from Common.Requirements.session_req import require_session

def test_route(ns):

    @ns.route('/test')
    class Test(Resource):
        @ns.doc('test',
                description='Test route, returns OK if the API is running and the user is logged in.',
                responses={200: 'OK', 
                           400: 'Invalid Argument', 
                           500: 'Mapping Key Error'})
        #requirements
        @require_session
        #@require_admin_account  
        def get(self):
            return jsonify({"Test": "OK"})