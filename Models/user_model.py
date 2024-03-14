from flask_restx import fields


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
                required=True, description="Rapport type", example="MyRapport"
            ),
        },
    )

# defines rapport-insertion model
def insert_data_model(api):
    return api.model(
        "InsertData",
        {
            "table_name": fields.String(
                required=True, description="Name of the table where data will be inserted.", example="myTable"
            ),
            "data": fields.Raw(
                required=True, description="Data to be inserted into the table.", example= {"column1": "myValue", "column2": 1337}
            ),
        },
    )


# defines subuser model
def sub_leader_model(api):
    return api.model(
        "New leader user",
        {
            "email": fields.String(
                required=True, description="User email", example="paul.nordmann@viken.no"
            ),
            "password": fields.String(
                required=True, description="User password", example="EpicPassword420"
            ),
        },
    )

# defines subuser model
def sub_operator_model(api):
    return api.model(
        "New operator user",
        {
            "email": fields.String(
                required=True, description="User email", example="lars.nordmann@viken.no"
            ),
            "password": fields.String(
                required=True, description="User password", example="EpicPassword420"
            ),
            "rapportName": fields.String(
                required=True, description="Rapport name", example="BorreproveRapport_ola_nordmann_viken_no"
            ),
        },
    )

# defines data date num model
def data_date_num_model(api):
    return api.model(
        "Data date num",
        {
            "table_name": fields.String(
                required=True, description="Name of the table where data will be extracted.", example="myTable"
            ),
            "date_start": fields.String(
                required=False, description="Start date for extraction", example="1992-01-01"
            ),
            "date_stop": fields.String(
                required=False, description="Stop date for extraction", example="2025-01-31"
            ),
            "rapport_count": fields.String(
                required=False, description="Number of rapports", example="5"
            ),
        }
    )