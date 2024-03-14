from SQLAdminConnections import SQL_AdminConnector as SQLC
from SQLAdminConnections import SQL_AdminQuerys as SQLQ

def createNewLeaderUser(email, password, accountType,adminEmail,key):

        #sets up database name and email - Formats email to be used as database & table name
    databaseName = "db_"+adminEmail.replace("@", "_").replace(".", "_")
    onlyEmail = email.replace("@", "_").replace(".", "_")
    
    #makes object of SQLConAdmin class
    adminConnection = SQLC.SQLConAdmin()

    #sets up connector with admin credentials
    connection = adminConnection
    connection.connect()
    
    try:
        #Create the new user
        connection.execute_query(SQLQ.SQLQueries.create_user(email, key))
        print(email)
        print(key)
              
        #Grant the new user privileges on the new database
        query = SQLQ.SQLQueries.grant_leader_access(databaseName, email)
        connection.execute_query(query)
        
        #Flush privileges
        query = SQLQ.SQLQueries.flush_privileges()
        connection.execute_query(query)
        
        #Add user details to the users database
        connection.execute_query(SQLQ.SQLQueries.use_users_database())
        connection.execute_query(SQLQ.SQLQueries.save_user_credentials(email, password, accountType, databaseName, adminEmail))
        
        connection.cnx.commit()
        connection.close()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        connection.close()