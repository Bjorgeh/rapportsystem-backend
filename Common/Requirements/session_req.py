from functools import wraps
from USER_session import sessionhandler as SH
from flask import session

user_session = SH.UserSession(session, None)

#function for valid session requirement
def require_session(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if not user_session.is_authenticated():
            return {"Error": "No access or session expired"}, 401
        return func(*args, **kwargs)
    return wrapped

