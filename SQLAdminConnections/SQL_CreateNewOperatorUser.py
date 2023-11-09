from SQLAdminConnections import SQL_AdminConnector as SQLC
from SQLAdminConnections import SQL_AdminQuerys as SQLQ

def createNewOperatorUser(email, password,accountType):
    #makes object of SQLConAdmin class
    adminConnection = SQLC.SQLConAdmin()

    #sets up connector with admin credentials
    connection = adminConnection
    connection.connect()
    
    try:
        #Create the new user
        connection.execute_query(SQLQ.SQLQueries.create_user(email, password))

        #Add user details to the users database
        connection.execute_query(SQLQ.SQLQueries.use_users_database())
        connection.execute_query(SQLQ.SQLQueries.save_user_credentials(email, password, accountType))
        
        #Commit changes and close connection
        connection.cnx.commit()
        connection.close()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        connection.close()