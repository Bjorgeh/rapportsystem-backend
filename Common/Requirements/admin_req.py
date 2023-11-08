import os
current_directory = os.getcwd()
#imports sys
import sys
sys.path.append(os.path.join(current_directory))
from functools import wraps
from USER_obj.users import logged_in_user as USR

#function for valid accountType requirement
def require_admin_account(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if not USR.getAccountType() == "admin":
            return {"Error": "You need an Admin account for this."}, 401
        return func(*args, **kwargs)
    return wrapped