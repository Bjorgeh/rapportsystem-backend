from SQLAdminConnections import SQL_AdminConnector, SQL_AdminQuerys

def createNewLeaderUser(email, password, databaseName):
    #makes object of SQLConAdmin class
    adminConnection = SQL_AdminConnector.SQLConAdmin()
    #query object
    SQLQueries = SQL_AdminQuerys.SQLQueries()

    #sets up connector with admin credentials
    connector = adminConnection
    connector.connect()
    
    try:
        #Create the new user
        query = SQLQueries.create_user(email, password)
        connector.execute_query(query)
        
        #Create the new database
        query = SQLQueries.create_database(databaseName)
        connector.execute_query(query)
        
        #Grant the new user privileges on the new database
        query = SQLQueries.grant_access(databaseName, email)
        connector.execute_query(query)
        
        #Flush privileges
        query = SQLQueries.flush_privileges()
        connector.execute_query(query)
        
        #Add user details to the users database
        query = SQLQueries.use_users_database()
        connector.execute_query(query)

        query = SQLQueries.save_user_credentials(email, password, databaseName)
        connector.execute_query(query)

        connector.cnx.commit()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        connector.close()