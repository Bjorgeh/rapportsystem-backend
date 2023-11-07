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
    host_IP = 'YOUR MYSQL SERVER IP'
    host_user = 'YOUR USERNAME'
    host_password = 'YOUR PASSWORD'
    host_database = 'TARGET DATABASE'
    simple_query = 'YOUR SQL QUERY'
    ```

    If you are collaborating with others, you can download `secret.py` from the Teams chat.
