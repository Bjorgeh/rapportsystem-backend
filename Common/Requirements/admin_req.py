import os
from functools import wraps
from flask import session,jsonify

#function for valid accountType requirement
def require_admin_account(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"Error": "You need to be logged in for this."})
        
        if session['account_type'] != 'admin':
            return jsonify({"Error": "You need an Admin account for this."})
        
        return func(*args, **kwargs)
    return wrapped