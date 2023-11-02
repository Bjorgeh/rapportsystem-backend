from flask_restx import fields

#defines user model
def leader_user_model(api):
    return api.model('LeaderUser', {  # Changed model name to 'LeaderUser'
        'email': fields.String(required=True, description='User email'),
        'userPass': fields.String(required=True, description='User password'),
        'databaseName': fields.String(required=True, description='Database name for the user')
    })

#defines user model
def operator_user_model(api):
    return api.model('OperatorUser', {  # Changed model name to 'OperatorUser'
        'email': fields.String(required=True, description='User email'),
        'userPass': fields.String(required=True, description='User password')
    })