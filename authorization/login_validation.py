import os
import sys

current_directory = os.getcwd()
sys.path.append(os.path.join(current_directory)) #path dir containing pw_manager.py
from PW_hashHandler import pw_manager as PW
from SQLAdminConnections import SQL_AdminQuerys as SQLQ
from SQLAdminConnections import SQL_AdminConnector as SQLC


#class for validating login credentials
class loginValidation:
    
    def __init__(self, username, clean_pw):
        self.username = username
        self.clean_pw = clean_pw
        
    #defines validation function
    def validate_credentials(self):
        #makes object of SQLConAdmin class
        adminConnection = SQLC.SQLConAdmin()
        #sets up connector with admin credentials
        connection = adminConnection

        connection.connect()
        connection.execute_query(SQLQ.SQLQueries.use_users_database(), None)
        connection.execute_query(SQLQ.SQLQueries.get_hashed_password_and_id_by_username(self.username))
        
        #print(SQLQ.SQLQueries.get_hashed_password_and_id_by_username(self.username))
        result = connection.execute_query(SQLQ.SQLQueries.get_hashed_password_and_id_by_username(self.username))
        connection.close()

        # Initialize default values for the response list: [is_valid, user_id]
        response_list = [False, None, None]
        print(result)

        # If there's no result, the username is not in the database.
        if not result:
            return response_list

        # Extract user ID and hashed password from result
        user_id, hashed_pw,accountType = result[0]

        # Validate password
        if PW.check(self.clean_pw, hashed_pw):
            response_list[0] = True  # Set is_valid to True
            response_list[1] = user_id  # Set user_id
            response_list[2] = accountType
            
        print(response_list)
        return response_list




    
        

