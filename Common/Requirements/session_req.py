from functools import wraps
from USER_session import sessionhandler as SH
from flask import session,jsonify

#function for valid session requirement
def require_session(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        user_session = SH.UserSession(session)
        auth = user_session.is_authenticated() #Gets the authentication status
        if not auth.get("AUTH", False):
            return jsonify({"Error": "No access or session expired", "Message": auth})
        return func(*args, **kwargs)
    return wrapped


