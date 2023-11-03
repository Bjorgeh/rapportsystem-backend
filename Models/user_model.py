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
    return api.model('OperatorUser', { 
        'username': fields.String(required=True, description='User email'),
        'password': fields.String(required=True, description='User password')
    })


#defines login model
def user_model(api):
    return api.model('newUser', { 
        'email': fields.String(required=True, description='User email'),
        'password': fields.String(required=True, description='User password'),
        'accountType': fields.String(required=True, description='Account type')
    })

