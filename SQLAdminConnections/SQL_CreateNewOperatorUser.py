from SQLAdminConnections import SQL_AdminConnector, SQL_AdminQuerys

def createNewOperatorUser(email, password):
    #makes object of SQLConAdmin class
    adminConnection = SQL_AdminConnector.SQLConAdmin()
    #query object
    SQLQueries = SQL_AdminQuerys.SQLQueries()

    #sets up connector with admin credentials
    connector = adminConnection
    connector.connect()
    
    try:
        #Create the new user
        query, params = SQLQueries.create_user(email, password)
        connector.execute_query(query, params)
        
        #Add user details to the users database
        query = SQLQueries.use_users_database()
        connector.execute_query(query)

        query, params = SQLQueries.save_user_credentials(email, password, "NULL")
        connector.execute_query(query, params)

        connector.cnx.commit()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        connector.close()