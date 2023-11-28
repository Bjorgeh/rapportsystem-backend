from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt
from USER_session import tokenHandler as TH
from Common.Requirements import valid_token as vt

# Get request for logout
def logout_route(ns):
    @ns.route('/logout')
    class logout(Resource):
        @ns.doc('Logout',
                description='Logout route, marks user token as revoked and returns a goodbye message.',
                responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})
        
        #Requires valid jwt token
        @jwt_required()
        @vt.require_valid_token

        def get(self):
            user_token = TH.UserTokenHandler()
            #logs out the user
            success = user_token.logout()
            return {"Goodbye": "See you again soon!", "Logout": success}, 200
