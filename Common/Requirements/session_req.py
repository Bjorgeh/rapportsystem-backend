from functools import wraps
from USER_session import sessionhandler as SH
from flask import session


#function for valid session requirement
def require_session(func):
    user_session = SH.UserSession(session)
    @wraps(func)
    def wrapped(*args, **kwargs):
        if not user_session.is_authenticated():
            user_session.logout()
            return {"Error": "No access or session expired"}, 401
        return func(*args, **kwargs)
    return wrapped

