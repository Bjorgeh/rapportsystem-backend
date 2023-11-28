#Importing the required modules
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps

#Function that checks if the user is an admin
def require_admin_account(func):
    @wraps(func)
    #requires a token
    @jwt_required()  
    def wrapped(*args, **kwargs):
        #gets the current user and checks if the account type is admin
        current_user = get_jwt_identity()
        if current_user['accountType'] != 'admin':
            return {"Error": "You need an Admin account for this."}, 403
        return func(*args, **kwargs)
    return wrapped
