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
                required=True, description="Name of the rapport where data will be inserted. Get your rapportname from: /api/user/get/rapportInfo", example="BorreproveRapport"
            ),
            "data": fields.Raw(
                required=True, description="Data to be inserted into the table. Note: Date, Time & ID will be autoincremented in rapport, can't be added via request.", example= {"part_type": "some_part_type","stove": "some_stove","catalog_number": 123,"test_amount": 5,"ordrer_number": "some_order_number","approved": True,"sign": "some_sign"}
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
                required=True, description="User password", example="EpicPassword69"
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
                required=True, description="User password", example="EpicPassword69"
            ),
            "rapportName": fields.String(
                required=True, description="Rapport name", example="BorreproveRapport"
            ),
        },
    )

# defines data date num model
def data_date_num_model(api):
    return api.model(
        "Data date num",
        {
            "table_name": fields.String(
                required=True, description="Name of the table where data will be extracted.", example="BorreproveRapport"
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

# defines last report deletion model
def remove_last_row(api):
    return api.model(
        "Remove last row",
        {
            "table_name": fields.String(
                required=True, description="Name of the rapport where last data will be removed. Get your rapportname from: /api/user/get/rapportInfo", example="BorreproveRapport"
            )
        }
    )


# defines rapport-insertion model
def update_table_data_model(api):
    return api.model(
        "update data",
        {
            "table_name": fields.String(
                required=True, description="Name of the rapport where data will be inserted. Get your rapportname from: /api/user/get/rapportInfo\nNote: Date, Time & ID will be autoincremented in rapport, don't add via request.", example="BorreproveRapport"
            ),
            "data": fields.Raw(
                required=True, description="Data to be updated.", example= {"part_type": "some_part_type","stove": "some_stove","catalog_number": 123,"test_amount": 5,"ordrer_number": "some_order_number","approved": True,"sign": "some_sign"}
            ),
        },
    )