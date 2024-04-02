# Importing the required modules
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps

# Function that checks if the user is either a leader or an admin
def require_leader_or_admin_account(func):
    @wraps(func)
    # Requires a token
    @jwt_required()
    def wrapped(*args, **kwargs):
        # Gets the current user and checks if the account type is either leader or admin
        current_user = get_jwt_identity()
        if current_user['accountType'] not in ['leader', 'admin']:
            return {"Error": "You need either a leader or admin account for this."}, 403
        return func(*args, **kwargs)

    return wrapped

