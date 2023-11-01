from flask_restx import fields

#defines user model
def user_model(api):
    return api.model('User', {
        'email': fields.String(required=True, description='User email'),
        'userPass': fields.String(required=True, description='User password'),
        'databaseName': fields.String(required=True, description='Database name for the user')
    })