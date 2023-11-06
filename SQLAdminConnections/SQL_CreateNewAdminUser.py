from SQLAdminConnections import SQL_AdminConnector as SQLC
from SQLAdminConnections import SQL_AdminQuerys as SQLQ

def createNewAdminUser(email, password, accountType):
    #makes object of SQLConAdmin class
    adminConnection = SQLC.SQLConAdmin()

    #sets up connector with admin credentials
    connection = adminConnection
    connection.connect()
    
    try:
        #Create the new user
        connection.execute_query(SQLQ.SQLQueries.create_user(email, password))
        
        #Create the new database
        #query = SQLQueries.create_database(databaseName)
        #connector.execute_query(query)
        
        #Grant the new user privileges on the new database
        #query = SQLQueries.grant_access(databaseName, email)
        #connector.execute_query(query)
        
        #Flush privileges
        #query = SQLQueries.flush_privileges()
        #connector.execute_query(query)
        
        #Add user details to the users database
        #Add user details to the users database

        connection.execute_query(SQLQ.SQLQueries.use_users_database())

        connection.execute_query(SQLQ.SQLQueries.save_user_credentials(email, password, accountType))
        
        connection.cnx.commit()
        
        connection.close()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        connection.close()