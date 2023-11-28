#importing the required modules
from functools import wraps
from USER_session import tokenHandler as TH
from flask_jwt_extended import jwt_required

#function for valid session requirement
def require_valid_token(func):
    current_user = TH.UserTokenHandler()
    @wraps(func)
    def wrapped(*args, **kwargs):
        #gets the current user and checks if token is valid
        auth = current_user.is_authenticated() 
        if not auth.get("AUTH", False):
            return {"Error": "No access or session expired", "Message": auth}
        return func(*args, **kwargs)
    return wrapped


