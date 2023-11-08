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

    You can install them using pip:
    ```
    pip install mysql-connector-python Flask flask-restx flask-session bcrypt
    ```

3. Create a secret file at `./SQLConnections/secret.py` with the following content:
    ```
    host_IP = 'DATABASE IP
    host_user = 'USERNAME'
    host_password = 'YOUR PASSWORD'
    host_database = None
    host_userdatabase = "DATABASE NAME"
    host_users_table = "user_info"
    host_session_table = "session_info"

    #Sets app config. This is used in API.py
    def setConfig(app):
        app.config['SECRET_KEY'] = 'TESTKEY'
        app.config['SESSION_TYPE'] = 'filesystem'
        return 1
    ```

    If you are collaborating with others, you can download `secret.py` from the Teams chat.
