# rapportsystem-backend

Before cloning the repository, make sure to follow these steps:

1. Install pip:
    ```
    python3 get-pip.py
    ```

2. Install the following packages:
    - mysql-connector-python
    - Flask
    - flask-restx
    - flask-session
    - bcrypt
    - httpagentparser
    - flask-cors

    You can install them using pip:
    ```
    pip install mysql-connector-python Flask flask-restx flask-session bcrypt flask-cors httpagentparser
    ```

3. Create a secret file at `./SQLConnections/secret.py` with the following content:
    ```
    host_IP = 'YOUR DB IP'
    host_user = 'ADMIN USER'
    host_password = 'ADMIN PASSWORD'
    host_database = None
    host_userdatabase = "users"
    host_users_table = "user_info"
    host_session_table = "tokens"
    
    # Sets app config. This is used in API.py
    def setConfig(app):
    app.config['SECRET_KEY'] = 'TESTKEY'
    app.config['JWT_SECRET_KEY'] = 'SUPER_SECRET_KEY' 
    return 1

    ```

    If you are collaborating with others, you can download `secret.py` from the Teams chat.
