import mysql.connector
import sys
import os
current_directory = os.getcwd()
print(current_directory)

sys.path.append(os.path.join(current_directory)) #path dir containing secret.py
from SQLConnections import secret as S


#Class for connecting to SQL database as Admin
class SQLConAdmin:
    def __init__(self, IP= None, USR= None, PW= None, DB= None):
        if IP is None:
            self.IP = S.host_IP
        else:
            self.IP = IP
        if USR is None:
            self.USR = S.host_user
        else:
            self.USR = USR
        if PW is None:
            self.PW = S.host_password
        else:
            self.PW = PW
        if DB is None:
            self.DB = S.host_database
        else:
            self.DB = DB
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
    def setUser(self, username, password, database):
        self.USR = username
        self.PW = password
        self.DB = database
        print("User set to: ", self.USR, "Database set to: ", self.DB)
    
    def getConnectionInfo(self):
        return self.IP, self.USR, self.PW, self.DB
    
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
            print("Connected to the database!")
            
        # If connection fails, print error
        except mysql.connector.Error as err:
            print("koden stopper her...")
            print(f"Error: {err}")
            self.close()
            
            return self  # <- Return the instance of the class after connection is made

    def execute_query(self, query_with_params, params=None):
        print(query_with_params)
        try:
            # Checks if connection is established
            if not self.cnx:
                print("Not connected to the database!")
                return

            # Handle cases where only a query is provided
            if len(query_with_params) == 1:
                query = query_with_params[0]
                params = None
            else:
                query, params = query_with_params

            # Execute query with parameters
            self.cursor.execute(query, params)  # <- Use self.cursor here

            if self.cursor.with_rows:   # <- And here as well
                result = self.cursor.fetchall()  # <- And here
            else:
                result = None

            return result

        # If execution fails, print error
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    #closes connection and cursor
    def close(self):
        if self.cursor:
            try:
                self.cursor.close()
                print("Cursor closed")
            except Exception as e:
                print(f"Error closing cursor: {e}")

        if self.cnx:
            try:
                self.cnx.close()
                print("Connection closed")
            except Exception as e:
                print(f"Error closing connection: {e}")
