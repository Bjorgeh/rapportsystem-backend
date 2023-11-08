import os
from functools import wraps
from flask import session

#function for valid accountType requirement
def require_admin_account(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return {"Error": "You need to be logged in for this."}, 401
        
        if session['account_type'] != 'admin':
            return {"Error": "You need an Admin account for this."}, 401
        
        return func(*args, **kwargs)
    return wrapped