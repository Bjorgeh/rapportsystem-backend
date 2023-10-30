'''import mysql.connector
from secret import *

#Function connects and sends query to SQL database
def createNewDatabase(IP, USR, PW, DB, newDB):
    cursor = None
    cnx = None

    try:
        # setting up the connection to HOPRO database
        cnx = mysql.connector.connect(
            host=IP,           # mySQL server IP
            user=USR,         # username
            password=PW,    # Password
            database=DB  # Database
        )

        # Creates cursor for making SQL-queries
        cursor = cnx.cursor()

        # Execute a simple query
        cursor.execute("CREATE DATABASE {};".format(newDB))

        # gets result from query & prints
        result = cursor.fetchone()
        print(result)

    # If connection fails, print error
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    # closes cursor if error occurs
    finally:
        if cursor:
            try:
                cursor.close()
            except Exception as e:
                print(f"Error closing cursor: {e}")
        
        if cnx:
            try:
                cnx.close()
            except Exception as e:
                print(f"Error closing connection: {e}")

#Function calls connectSQL with the parameters from secret.py
#createNewDatabase(host_IP, host_user, host_password, host_database, newDBname)
'''
