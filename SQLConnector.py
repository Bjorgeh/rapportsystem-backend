import mysql.connector
from secret import *

#Function connects and sends query to SQL database
def connectSQL(IP, USR, PW, DB, query):

    cursor = None
    cnx = None

    try:
        # setting up the connection to HOPRO database
        cnx = mysql.connector.connect(
            host=IP,           # Google VM instance IP
            user=USR,         # Admin user
            password=PW, # Password for admin user
            database=DB  # Database name
        )

        # Creates cursor for making SQL-queries
        cursor = cnx.cursor()

        # Execute a simple query
        cursor.execute(query)

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
connectSQL(host_IP, host_user, host_password, host_database, simple_query)