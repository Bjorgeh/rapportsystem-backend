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
    - flask-jwt-extended

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

4. Using the API in browser:
   
   - Run API.py
   - http://127.0.0.1:5001/api/
   - Create user
    ![image](https://github.com/Bjorgeh/rapportsystem-backend/assets/122554284/7158ae72-527f-4981-ac10-bdaf2e0d83aa)

   - Login
   ![image](https://github.com/Bjorgeh/rapportsystem-backend/assets/122554284/13f1385e-fbd2-41f5-a038-73eedbf5d14a)

   - Add your bearer Token from the login response:
   ![image](https://github.com/Bjorgeh/rapportsystem-backend/assets/122554284/8f211927-f7ec-4217-9f10-8b59aef3a929)

   - Auth:
   ![image](https://github.com/Bjorgeh/rapportsystem-backend/assets/122554284/afff75f4-7a1f-4fa8-924d-e3018260bf6f)
   ![image](https://github.com/Bjorgeh/rapportsystem-backend/assets/122554284/b83ac38b-ffad-49cc-9791-37938edde0e4)

   - You now have access to the functionality of the usertype of your account.
   
