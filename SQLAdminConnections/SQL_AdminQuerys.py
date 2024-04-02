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
    def save_user_credentials(email, password, accountType, databaseName='None', adminEmail='None'):
        # Assuming password is already hashed before calling this method
        query = "INSERT INTO user_info(email, userPass, accountType,databaseName,creator_name) VALUES (%s, %s, %s, %s,%s);"
        params = (email, password,accountType,databaseName,adminEmail)
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
    
    @staticmethod
    def insert_user_activity(user_id, ip_address, user_agent, operating_system):
        query = "INSERT INTO user_activity (user_id, ip_address, user_agent, operating_system) VALUES (%s, %s, %s, %s);"
        params = (user_id, ip_address, user_agent, operating_system)
        return query, params
    
    @staticmethod
    def delete_activities_older_than_30_days(user_id):
        query = "DELETE FROM user_activity WHERE user_id = %s AND activity_timestamp < NOW() - INTERVAL 30 DAY;"
        params = (user_id,)
        return query, params

    @staticmethod
    def delete_oldest_activity_if_needed(user_id):
        query = "DELETE FROM user_activity WHERE user_id = %s AND id IN (SELECT id FROM user_activity WHERE user_id = %s ORDER BY activity_timestamp ASC LIMIT 1 OFFSET 4);"
        params = (user_id, user_id)
        return query, params
    
    @staticmethod
    def get_oldest_activity_id_to_delete(user_id):
        query = "SELECT id FROM user_activity WHERE user_id = %s ORDER BY activity_timestamp ASC LIMIT 1 OFFSET 4;"
        params = (user_id,)
        return query, params

    @staticmethod
    def delete_activity_by_id(activity_id):
        query = "DELETE FROM user_activity WHERE id = %s;"
        params = (activity_id,)
        return query, params
    
    @staticmethod
    def get_oldest_activities(user_id):
        query = "SELECT * FROM user_activity WHERE user_id = %s ORDER BY activity_timestamp ASC LIMIT 5;"
        params = (user_id,)
        return query, params
    
    @staticmethod
    def get_user_information_by_id(user_id):
        query = "SELECT * FROM user_info WHERE id = %s;"
        params = (user_id,)
        return query, params
    
    @staticmethod
    def count_user_activities(user_id):
        query = "SELECT COUNT(*) FROM user_activity WHERE user_id = %s;"
        params = (user_id,)
        return query, params

    @staticmethod
    def get_oldest_activity_id(user_id):
        query = "SELECT id FROM user_activity WHERE user_id = %s ORDER BY activity_timestamp ASC LIMIT 1;"
        params = (user_id,)
        return query, params
    
    '''TOKEN-UPDATE FROM HERE ON'''
    
    # Inserts a new JWT token ID and associated user ID into the tokens table
    @staticmethod
    def insert_token_id(token_id, user_id):
        query = "INSERT INTO tokens (token_id, user_id, expiration) VALUES (%s, %s, NOW() + INTERVAL 1 DAY);"
        params = (token_id, user_id)
        return query, params

    # Checks if a given JWT token is valid and not revoked based on the token_id in the tokens table
    @staticmethod
    def check_token_validity(token_id):
        query = ("SELECT CASE WHEN expiration > CURRENT_TIMESTAMP AND revoked = FALSE THEN 1 ELSE 0 END AS is_valid FROM tokens WHERE token_id = %s;")
        params = (token_id,)
        return query, params

    # Marks a given JWT token as revoked in the tokens table
    @staticmethod
    def revoke_tokens_by_user_id(user_id):
        query = "UPDATE tokens SET revoked = TRUE WHERE user_id = %s;"
        params = (user_id,)
        return query, params

    # Deletes expired tokens from the tokens table
    @staticmethod
    def delete_expired_tokens():
        query = "DELETE FROM tokens WHERE expiration < CURRENT_TIMESTAMP;"
        return query, None
    
    # Gets ID from user_info by email
    @staticmethod
    def get_user_id_by_email(email):
        query = "SELECT id FROM user_info WHERE email = %s;"
        params = (email,)
        return query, params

    # Deletes token by user_id
    @staticmethod
    def delete_tokens_by_user_id(user_id):
        query = "DELETE FROM tokens WHERE user_id = %s;"
        params = (user_id,)
        return query, params

    #deletes activity by user_id
    @staticmethod
    def delete_activities_by_user_id(user_id):
        query = "DELETE FROM user_activity WHERE user_id = %s;"
        params = (user_id,)
        return query, params
    
    '''Creating rapports for user'''
    
    # use database
    @staticmethod
    def use_database(dbname):
        query = f"USE {dbname};"
        return query, None

    # create table -> custom
    @staticmethod
    def create_table(table_name):
        query = "CREATE TABLE %s ();"
        params = (table_name,)
        return query, params
    
    #add column to table -> custom
    @staticmethod
    def add_column(table_name, column_name, column_type, prim_or_foreignKey = None):
        if prim_or_foreignKey is None:
            query = "ALTER TABLE %s ADD COLUMN %s %s;"
            params = (table_name, column_name, column_type)
        else:
            query = "ALTER TABLE %s ADD COLUMN %s %s %s;"
            params = (table_name, column_name, column_type, prim_or_foreignKey)
        return query, params

    @staticmethod
    def create_disa_table(table_name):
        query = f"CREATE TABLE {table_name} (id INT NOT NULL AUTO_INCREMENT, shift VARCHAR(45) NOT NULL, date DATE DEFAULT CURRENT_DATE, time TIME DEFAULT CURRENT_TIME, amt_formed INT NOT NULL, amt_cast INT NOT NULL, model_number INT NOT NULL, comment VARCHAR(250), sign VARCHAR(20) NOT NULL, PRIMARY KEY (id), UNIQUE INDEX id_UNIQUE (id ASC) VISIBLE);"
        return query, None

    @staticmethod
    def create_sandAnalyseRapport_table(table_name):
        query = f"CREATE TABLE {table_name} (id INT NOT NULL AUTO_INCREMENT, date DATE DEFAULT CURRENT_DATE, time TIME DEFAULT CURRENT_TIME, moisture DECIMAL NOT NULL, pressure_strengt DECIMAL NOT NULL, packing_degree DECIMAL NOT NULL, burn_out DECIMAL NOT NULL, shear_strength DECIMAL NOT NULL, active_bentonie DECIMAL NOT NULL, sludge_content DECIMAL NOT NULL, sieve_analysis DECIMAL NOT NULL, compressibility DECIMAL NOT NULL, sand_temp DECIMAL NOT NULL, signature VARCHAR(20) CHARACTER SET utf16 NOT NULL, PRIMARY KEY (id), UNIQUE INDEX id_UNIQUE (id ASC) VISIBLE);"
        return query, None

    @staticmethod
    def create_skrapRapport_table(table_name):
        query = f"CREATE TABLE {table_name} (id INT NOT NULL AUTO_INCREMENT, date DATE DEFAULT CURRENT_DATE, time TIME DEFAULT CURRENT_TIME, catalog_number INT NOT NULL, amount_ordered INT NOT NULL, amount_lacking INT NOT NULL, price_pr_piece FLOAT NULL, sum_price FLOAT GENERATED ALWAYS AS (amount_lacking * price_pr_piece) VIRTUAL, PRIMARY KEY (id), UNIQUE INDEX id_UNIQUE (id ASC) VISIBLE);"
        return query, None

    @staticmethod
    def create_smelteRapport_table(table_name):
        query = f"CREATE TABLE {table_name} (id INT NOT NULL AUTO_INCREMENT, furnace_number INT NOT NULL, date DATE DEFAULT CURRENT_DATE, time TIME DEFAULT CURRENT_TIME, kg_returns FLOAT NOT NULL, kg_scrap_metal FLOAT NOT NULL, total_weight_melt FLOAT GENERATED ALWAYS AS (kg_returns + kg_scrap_metal) VIRTUAL, kg_carbon FLOAT NOT NULL, kg_ore FLOAT NOT NULL, kg_fesi FLOAT NOT NULL, kg_fep FLOAT NOT NULL, kwh_pre_melt DOUBLE NOT NULL, kwh_post_melt DOUBLE NOT NULL, sum_kwh_used DOUBLE GENERATED ALWAYS AS (kwh_pre_melt - kwh_post_melt) VIRTUAL, PRIMARY KEY (id), UNIQUE INDEX id_UNIQUE (id ASC) VISIBLE);"
        return query, None

    @staticmethod
    def create_borreproverapport_table(table_name):
        query = f"CREATE TABLE {table_name} (id INT NOT NULL AUTO_INCREMENT, part_type VARCHAR(45) NOT NULL, stove VARCHAR(45) NOT NULL, catalog_number INT NULL, test_amount INT NULL, ordrer_number VARCHAR(45) NOT NULL, approved BOOL NOT NULL, date DATE DEFAULT CURRENT_DATE, time TIME DEFAULT CURRENT_TIME, sign VARCHAR(20) NOT NULL, PRIMARY KEY (id), UNIQUE INDEX id_UNIQUE (id ASC) VISIBLE);"
        return query, None

    @staticmethod
    def getTableDescription(table_name):
        query = f"DESCRIBE {table_name};"
        return query, None
    
    @staticmethod
    def getAllFromTable(table_name):
        query = f"SELECT * FROM {table_name};"
        return query, None
    
    @staticmethod
    def show_tables():
        return "SHOW TABLES;", None
    
    @staticmethod
    def insert_into_table(table_name, data):
        columns = ', '.join(data.keys())
        values = ', '.join(['%s' if value is not None else 'NULL' for value in data.values()])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"
        params = tuple(value if value is not None else None for value in data.values())  # None for 'NULL'
        return query, params
    
    @staticmethod
    def grant_leader_access(database_name,user_id):
        query = f"GRANT SELECT, INSERT, UPDATE, DELETE ON {database_name}.* TO '{user_id}'@'%';"
        return query, None
        
    @staticmethod
    def grant_operator_access(database_name, table_name, user_id):
        query = f"GRANT SELECT, INSERT ON {database_name}.{table_name} TO '{user_id}'@'%';"
        return query, None

    @staticmethod
    def get_database_name(email):
        query = "SELECT databaseName FROM user_info WHERE email = %s;"
        params = (email,)
        return query, params
    
    @staticmethod
    def get_data_between_dates(table_name, start_date, stop_date):
        query = f"SELECT * FROM {table_name} WHERE date >= %s AND date <= %s;"
        params = (start_date, stop_date)
        return query, params

    @staticmethod
    def limit_query(table_name, num_rows):
        query = f"SELECT * FROM {table_name} LIMIT {num_rows};"
        return query, None
    
    @staticmethod
    def get_pw(email):
        query = "SELECT userPass FROM user_info WHERE email = %s;"
        params = (email,)
        return query, params
    
    @staticmethod
    def get_last_inserted_id(table_name):
        query = f"SELECT MAX(id) FROM {table_name};"
        return query, None

    @staticmethod
    def update_last_row_by_id(table_name, data):
        update_values = ', '.join([f"{key} = %s" for key in data.keys()])
        query = f"UPDATE {table_name} SET {update_values} ORDER BY id DESC LIMIT 1;"
        params = tuple(data.values())
        return query, params

    @staticmethod
    def delete_last_row_by_id(table_name):
        query = f"DELETE FROM {table_name} ORDER BY id DESC LIMIT 1;"
        return query, None
    
    @staticmethod
    def get_last_row_by_id(table_name):
        query = f"SELECT * FROM {table_name} ORDER BY id DESC LIMIT 1;"
        return query, None

    @staticmethod
    def get_all_sub_users(email):
        query = "SELECT email, accountType FROM user_info WHERE creator_name = %s;"
        params = (email,)
        return query, params


