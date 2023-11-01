import mysql.connector
import sys
sys.path.append('C:/rapportsystem-backend/SQLAdminConnections') #path dir containing secret.py
import secret as S

#Class for connecting to SQL database as Admin
class SQLConAdmin:
    def __init__(self):
        self.IP = S.host_IP
        self.USR = S.host_user
        self.PW = S.host_password
        self.DB = S.host_database
        self.cnx = None
        self.cursor = None

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
    def execute_query(self, query):
        try:
            #Checks if connection is established
            if not self.cnx or not self.cursor:
                print("Not connected to the database!")
                return

            #Execute query
            self.cursor.execute(query)
            return self.cursor.fetchall()

        # If connection fails, print error
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
