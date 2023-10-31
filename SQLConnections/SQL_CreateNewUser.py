import mysql.connector
#from SQLConnections import secret as S #if this wont work, try the next import instead
import sys
sys.path.append('C:/rapportsystem-backend/SQLConnections') #path dir containing secret.py
import secret as S #if this wont work, try the above import instead

'''from secret import (
    host_IP,host_database,host_password,host_user,host_userdatabase,simple_query
)'''

#Function connects and sends query to SQL database, adds new SQL user, database and grants privileges
def createNewUser(email, password, databaseName):

    #Adds new user to SQL, creates database and grants privileges
    createSQLUser(email, password, databaseName)

    #createNewUser("testuser", "testpassword", "testDB")

'''
Function calls connectSQL with the parameters from secret.py and new username and password, 
creates database and grants privileges to the users own database only.
'''

def createSQLUser(newUsername, newUserpassword, databaseName):

    #adds user info to users database
    addUserToDatabase(newUsername, newUserpassword, databaseName)

    cursor = None
    cnx = None
    try:
        # setting up the connection to HOPRO database
        cnx = mysql.connector.connect(
            host=S.host_IP,           # mySQL server IP
            user=S.host_user,         # username
            password=S.host_password,    # Password
            database=S.host_database  # Database
        )

        # Creates cursor for making SQL-queries
        cursor = cnx.cursor()

        # Executes a simple query
        #cursor.execute("CREATE USER '{}'@'%' IDENTIFIED BY '{}'; CREATE DATABASE {}; GRANT ALL PRIVILEGES ON {}.* TO '{}'@'%';FLUSH PRIVILEGES;".format(newUsername, newUserpassword, databaseName, databaseName, newUsername))

        # Create the user
        cursor.execute("CREATE USER '{}'@'%' IDENTIFIED BY '{}';".format(newUsername, newUserpassword))

        # Create the database
        cursor.execute("CREATE DATABASE {};".format(databaseName))

        # Grant privileges to the new user
        cursor.execute("GRANT ALL PRIVILEGES ON {}.* TO '{}'@'%';".format(databaseName, newUsername))

        # Flush privileges
        cursor.execute("FLUSH PRIVILEGES;")

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

#Adds user to the users database
def addUserToDatabase(newUsername, newUserpassword, databaseName):
    cursor = None
    cnx = None

    try:
        # setting up the connection to HOPRO database
        cnx = mysql.connector.connect(
            host=S.host_IP,           # mySQL server IP
            user=S.host_user,         # username
            password=S.host_password,    # Password
            database=S.host_userdatabase  # Database
        )

        # Creates cursor for making SQL-queries
        cursor = cnx.cursor()

        # Selects the user table
        cursor.execute("USE users;")

        data = (newUsername, newUserpassword, databaseName)
        query = "INSERT INTO users_info(email, userPass, databaseName) VALUES (%s,%s,%s);"
        cursor.execute(query, data)

        cnx.commit()

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

#createNewUser()