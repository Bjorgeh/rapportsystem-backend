import mysql.connector
import sys
import os
current_directory = os.getcwd()
print(current_directory)

sys.path.append(os.path.join(current_directory)) #path dir containing secret.py
from SQLConnections import secret as S


#Class for connecting to SQL database as Admin
class SQLConAdmin:
    def __init__(self):
        self.IP = S.host_IP
        self.USR = S.host_user
        self.PW = S.host_password
        self.DB = S.host_database
        self.cnx = None
        self.cursor = None

    '''
    def ip(self):
        return self.IP
    def usr(self):
        return self.USR
    def pw(self):
        return self.PW
    def db(self):
        return self.DB
    '''
    
    #connects to SQL database
    def connect(self):
        try:
            # setting up the connection to the database
            self.cnx = mysql.connector.connect(
                host=self.IP,
                user=self.USR,
                password=self.PW,
                database=self.DB
            )
            self.cursor = self.cnx.cursor()

        # If connection fails, print error
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.close()

    #execute query and return result
    def execute_query(self, query_with_params, params=None):
        try:
            # Checks if connection is established
            if not self.cnx:
                print("Not connected to the database!")
                return

            cursor = self.cnx.cursor()
            
            # Handle cases where only a query is provided
            if len(query_with_params) == 1:
                query = query_with_params[0]
                params = None
            else:
                query, params = query_with_params

            # Execute query with parameters
            cursor.execute(query, params)

            if cursor.with_rows:
                result = cursor.fetchall()
            else:
                result = None
            cursor.close()

            return result
    
        # If execution fails, print error
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    #closes connection and cursor
    def close(self):
        if self.cursor:
            try:
                self.cursor.close()
            except Exception as e:
                print(f"Error closing cursor: {e}")

        if self.cnx:
            try:
                self.cnx.close()
            except Exception as e:
                print(f"Error closing connection: {e}")
