import mysql.connector
from secret import * 

#Function connects and sends query to SQL database, adds new SQL user, database and grants privileges
def createNewUser():

    #Adds new user to SQL, creates database and grants privileges
    createSQLUser("testPerson@gmail.com", "superSecretPassword", "Jotul")

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
            host=host_IP,           # mySQL server IP
            user=host_user,         # username
            password=host_password,    # Password
            database=host_database  # Database
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
            host=host_IP,           # mySQL server IP
            user=host_user,         # username
            password=host_password,    # Password
            database=host_userdatabase  # Database
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