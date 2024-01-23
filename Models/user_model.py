from flask_restx import fields

"""'
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
"""


# defines login model
def login_model(api):
    return api.model(
        "Login",
        {
            "username": fields.String(
                required=True, description="User email", example="ola.nordmann@viken.no"
            ),
            "password": fields.String(
                required=True, description="User password", example="EpicPassword69"
            ),
        },
    )

# defines user model
def user_model(api):
    return api.model(
        "New user",
        {
            "email": fields.String(
                required=True, description="User email", example="ola.nordmann@viken.no"
            ),
            "password": fields.String(
                required=True, description="User password", example="EpicPassword69"
            ),
            "accountType": fields.String(
                required=True,
                description="Account type | admin/leader/operator",
                example="operator",
            ),
        },
    )


# defines pw model
def update_password_model(api):
    return api.model(
        "New password",
        {
            "password1": fields.String(
                required=True, description="New Password", example="EpicPassword69"
            ),
            "password2": fields.String(
                required=True,
                description="Confirmed Password",
                example="EpicPassword69",
            ),
        },
    )

# defines delete model
def delete_model(api):
    return api.model(
        "Delete user",
        {
            "username": fields.String(
                required=True, description="User email", example="ola.nordmann@viken.no"
            ),
            "password": fields.String(
                required=True, description="User password", example="EpicPassword69"
            ),
        },
    )

# defines rapport creation model
def create_rapport_model(api):
    return api.model(
        "Create rapport",
        {
            "rapportType": fields.String(
                required=True, description="Rapport type", example="Disa/Sandanalyse/Smelte/Skrap/Borreprove"
            ),
        },
    )