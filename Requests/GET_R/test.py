from flask_restx import Resource
#imports os
import os
current_directory = os.getcwd()
#imports sys
import sys
sys.path.append(os.path.join(current_directory))

from Common.Requirements.session_req import require_session
from Common.Requirements.admin_req import require_admin_account

def test_route(ns):
    @ns.route('/test')
    class Test(Resource):
        @ns.doc('test')
        #requirements
        @require_session
        #@require_admin_account  
        def get(self):
            return {"Test": "OK"}