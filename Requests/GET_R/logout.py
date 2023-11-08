from flask_restx import Resource
#imports os
import os
current_directory = os.getcwd()
#imports sys
import sys
sys.path.append(os.path.join(current_directory))
from USER_obj.users import logged_in_user
from flask import session
from USER_session import sessionhandler as SH
from Common.Requirements.session_req import require_session

#Get request for logout
def logout_route(ns):
    @ns.route('/logout')
    class logout(Resource):
        @ns.doc('Logout')
        @require_session
        def get(self):
            user_session = SH.UserSession(session, None)
            return {"Goodbye": "See you again soon!","Logout": user_session.logout(logged_in_user)}, 200
        
