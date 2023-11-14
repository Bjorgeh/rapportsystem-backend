import os
#Gets current directory
current_directory = os.getcwd()
#imports sys
import sys
sys.path.append(os.path.join(current_directory))
#Gets secret.py
from SQLConnections import secret as S

class SQLQueries:

    @staticmethod
    # Creates new database with given name
    def create_database(name):
        return f"CREATE DATABASE {name};", None

    @staticmethod
    # Creates new user with given name and password
    def create_user(usr, pw):
        return "CREATE USER %s@'%' IDENTIFIED BY %s;", (usr, pw)

    @staticmethod
    # Grants privileges to user to its own database
    def grant_access(database, usr):
        query = f"GRANT ALL PRIVILEGES ON {database}.* TO '{usr}'@'%';"
        return query, None

    @staticmethod
    # Refreshes the grant tables in the database (making new privileges effective)
    def flush_privileges():
        return f"FLUSH PRIVILEGES;", None

    @staticmethod
    # Switches to the users database for subsequent queries
    def use_users_database():
        return f"USE users;", None
    '''
    @staticmethod
    # Switches to the users database for subsequent queries
    def update_session_table():
        return f"UPDATE user_session;", None
    '''
    @staticmethod
    # Inserts new user credentials into the user_info table
    def save_user_credentials(email, password, accountType, databaseName='None'):
        # Assuming password is already hashed before calling this method
        query = "INSERT INTO user_info(email, userPass, accountType,databaseName) VALUES (%s, %s, %s, %s);"
        params = (email, password,accountType,databaseName)
        return query, params

    @staticmethod
    # Checks if a given session has expired based on the timestamp in the user_session table
    def check_session_expired(user_id):
        query = ("SELECT CASE WHEN expiration < CURRENT_TIMESTAMP THEN 1 ELSE 0 END AS has_expired FROM user_session WHERE user_id = %s;")
        params = (user_id,)
        return query, params

    @staticmethod
    # Inserts a new session ID and associated user ID into the user_session table
    def insert_session_id(session_id, user_id):
        query = query = "INSERT INTO user_session (session_id, user_id, expiration) VALUES (%s, %s, NOW() + INTERVAL 30 MINUTE)"
        params = (session_id, user_id)
        return query, params

    @staticmethod
    # Removes a given session ID from the user_session table
    def remove_session_id(session_id):
        query = "DELETE FROM user_session WHERE session_id = %s"
        params = (session_id,)
        return query, params

    @staticmethod
    # Retrieves session details for a given session ID from the user_session table
    def get_active_session(user_id):
        query = "SELECT * FROM user_session WHERE user_id = %s"
        params = (user_id,)
        return query, params
    
    #Gets hashed password
    @staticmethod
    def get_hashed_password_by_username(username):
        query = "SELECT userPass FROM user_info WHERE email = %s"
        params = (username,)
        return query, params
    
    #Gets id and hashed password
    @staticmethod
    def get_hashed_password_and_id_by_username(username):
        query = "SELECT id, userPass, accountType FROM user_info WHERE email = %s"
        params = (username,)
        return query, params
    
    @staticmethod
    def update_session(session_id):
        query = "UPDATE user_session SET expiration = NOW() + INTERVAL 30 MINUTE WHERE session_id = %s;"
        params = (session_id,)
        return query, params
    
    @staticmethod
    def update_user_login_password(username, new_password):
        query = "UPDATE user_info SET userPass = %s WHERE id = %s;"
        params = (new_password, username,)
        return query, params
    
    @staticmethod
    def update_sql_user_password(username, new_password):
        query = "ALTER USER %s@%s IDENTIFIED BY %s;"
        params = (username,'%', new_password,)
        return query, params
    
    @staticmethod
    def delete_old_sessions_by_user_id(user_id):
        query = "DELETE FROM user_session WHERE user_id = %s;"
        params = (user_id,)
        return query, params

    @staticmethod
    def delete_user_from_user_info(user_id):
        query = "DELETE FROM user_info WHERE email = %s;"
        params = (user_id,)
        return query, params
    
    @staticmethod
    def delete_sql_user(username):
        query = "DROP USER %s@%s;"
        params = (username, '%')
        return query, params
    
    @staticmethod
    def drop_database(username):
        query = f"DROP DATABASE `DB_{username}`;"
        return query, None