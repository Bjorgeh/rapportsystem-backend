from flask import Flask, send_from_directory
from flask_restx import Api
from flask_cors import CORS
from datetime import timedelta
import os
import sys

current_directory = os.getcwd()
sys.path.append(os.path.join(current_directory))

# Import routes and logic
from Requests.GET_R import (
    test as get_test,
    test_admin as get_test_admin,
    logout as get_logout,
    userActivity as get_userActivity,
    userInfo as get_userInfo,
    extractData_admin as extract_data_from_database,
    tableDescription_admin as extract_table_description_from_database,
    test_leader as get_test_leader,
    test_operator as get_test_operator,
    tableDescription_users as get_users_table_description,
    getSubUsers_admin as get_subUsers_admin
)
from Requests.POST_R import (
    extractLastData_users as extract_latest_data_from_database,
    login as post_login,
    createUser as post_createUser,
    updatePassword as post_updatePassword,
    adminUpdateUsersPass as post_adminUpdateUsersPass,
    deleteUser as post_deleteUser,
    createRapport as post_createRapport,
    insertData as post_insertData,
    adminCreateSubLeader as post_createLeaderSubUser,
    adminCreateSubOperator as post_createOperatorSubUser,
    extractPreciseData as post_extractPreciseData,
    deleteLastRapport as post_deleteLastRapport,
    changeDataInRapport as post_changeDataInRapport,
    adminDeleteUser as post_adminDeleteUser
)

from SQLConnections import secret as Secret
from flask_jwt_extended import JWTManager

# Initialize Flask app and API
app = Flask(__name__, static_url_path='', static_folder='doc_files')

# Set Flask configuration using Secret module
Secret.setConfig(app)

# Initialize JWT
JWTManager(app)

# Set up CORS to allow requests from any origin (Open CORS)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# Define authorizations for Swagger documentation
authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Type in the *Bearer* space token'
    },
}

# Initialize Flask-RESTx API
api = Api(
    app,
    version='1.0',
    title='RapportSystem API Doc',
    description='Overview of the API endpoints.\n\nUsage:\n- Log in\n- Go to authorize\n- Type in the *Bearer* space access_token\n- Use the API\n\n<a href="https://bjorgeh.github.io/rapportsystem-backend/doc_files/index.html">Link to API documentation</a>',
    doc='/api/',
    authorizations=authorizations, 
    security='Bearer Auth'
)

# Define namespaces for different user roles
user_post = api.namespace('api/user/post', description='POST Endpoints')
user_get = api.namespace('api/user/get', description='GET Endpoints')
admin_post = api.namespace('api/admin/post', description='POST Endpoints')
admin_get = api.namespace('api/admin/get', description='GET Endpoints')
leader_post = api.namespace('api/leader/post', description='POST Endpoints')
leader_get = api.namespace('api/leader/get', description='GET Endpoints')
operator_post = api.namespace('api/operator/post', description='POST Endpoints')
operator_get = api.namespace('api/operator/get', description='GET Endpoints')

# Define routes for all users
get_test.test_route(user_get)
get_logout.logout_route(user_get)
get_userActivity.activity_route(user_get)
get_userInfo.uInfo_route(user_get)
get_users_table_description.extract_table_description(user_get)
post_login.login_route(user_post)
post_updatePassword.update_password_route(user_post)
post_createUser.create_user(user_post)
post_deleteUser.delete_user_route(user_post)
post_extractPreciseData.extract_by_date_or_count(user_post)
post_insertData.insert_data(user_post)

# Define routes for admin users
get_test_admin.test_admin_route(admin_get)
extract_data_from_database.extract_data_from_database(admin_get)
extract_table_description_from_database.extract_table_description_from_database(admin_get)
get_subUsers_admin.extractSubUsers(admin_get)
post_createLeaderSubUser.create_sub_leader(admin_post)
post_createOperatorSubUser.create_sub_operator(admin_post)
post_adminUpdateUsersPass.admin_update_password_route(admin_post)
post_adminDeleteUser.admin_delete_subuser_route(admin_post)

# Define routes for leader users
get_test_leader.test_leader_route(leader_get)
post_deleteLastRapport.delete_last_row(leader_post)
post_changeDataInRapport.change_data(leader_post)
extract_latest_data_from_database.extract_last_data_from_database(leader_post)

# Define routes for operator users
get_test_operator.test_operator_route(operator_get)

# Serve static documentation files
@app.route('/doc')
def serve_index():
    return send_from_directory('doc_files', 'index.html')

# Run the Flask application
if __name__ == "__main__":
    # Hosts the API on port 5001 and sets debug to True
    app.run(host='0.0.0.0', debug=True, port=5001)
