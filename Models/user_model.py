from flask_restx import fields
''''
#defines leader model
def leader_user_model(api):
    return api.model('LeaderUser', {  
        'email': fields.String(required=True, description='User email'),
        'userPass': fields.String(required=True, description='User password'),
        'databaseName': fields.String(required=True, description='Database name for the user')
    })

#defines operator model
def operator_user_model(api):
    return api.model('OperatorUser', {  
        'email': fields.String(required=True, description='User email'),
        'userPass': fields.String(required=True, description='User password')
    })
'''

#defines login model
def login_model(api):
    return api.model('Login', { 
        'username': fields.String(required=True, description='User email'),
        'password': fields.String(required=True, description='User password')
    })

#defines login model
def user_model(api):
    return api.model('New user', { 
        'email': fields.String(required=True, description='User email'),
        'password': fields.String(required=True, description='User password'),
        'accountType': fields.String(required=True, description='Account type | admin/leader/operator')
    })

#defines login model
def update_password_model(api):
    return api.model('New password', { 
        'password1': fields.String(required=True, description='New Password'),
        'password2': fields.String(required=True, description='Confirmed Password')
    })
