from flask_restx import Resource
from flask import request,session
#imports os
import os
current_directory = os.getcwd()
#imports sys
import sys
sys.path.append(os.path.join(current_directory))

from USER_session import sessionhandler as SH

from SQLAdminConnections import SQL_AdminConnector as SQLC
from SQLAdminConnections import SQL_AdminQuerys as SQLQ
from PW_hashHandler import pw_manager as hash
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
            
            return updatePassword(new_pass1, new_pass2), 200

#Function for updating password
def updatePassword(new_password1, new_password2):
    if not new_password1 == new_password2:
        return {"Password": "Does not match."}
    
    #Secures password with hash
    hashed_password = hash.hash(new_password1)
    
    #Updates user password.
    connection = SQLC.SQLConAdmin()
    connection.connect()
    connection.execute_query(SQLQ.SQLQueries.use_users_database())
    connection.execute_query(SQLQ.SQLQueries.update_user_login_password(session['user_id'], hashed_password))
    connection.execute_query(SQLQ.SQLQueries.update_sql_user_password(session['email'], hashed_password))
    connection.execute_query(SQLQ.SQLQueries.flush_privileges())
    connection.cnx.commit()
    connection.close()

    #Logs out user after password changed
    current_user = SH.UserSession(session)
    current_user.logout()

    #Returns success if password is updated
    return {"Passwrod": "Updated!", "New password": "PROTECTED"}