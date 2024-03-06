from SQLAdminConnections import SQL_AdminConnector as SQLC
from SQLAdminConnections import SQL_AdminQuerys as SQLQ

import os
import sys
current_directory = os.getcwd()
sys.path.append(os.path.join(current_directory))
from Requests.CreateRapport import RapportMaker as RM


def createNewAdminUser(email, password, accountType):

    #sets up database name and email - Formats email to be used as database & table name
    databaseName = "db_"+email.replace("@", "_").replace(".", "_")
    onlyEmail = email.replace("@", "_").replace(".", "_")

    #makes object of SQLConAdmin class
    adminConnection = SQLC.SQLConAdmin()

    #sets up connector with admin credentials
    connection = adminConnection
    connection.connect()
    
    try:
        #Create the new user
        connection.execute_query(SQLQ.SQLQueries.create_user(email, password))
        
        #Create the new database
        query = SQLQ.SQLQueries.create_database(databaseName)
        connection.execute_query(query)

        #Use the new database
        query = SQLQ.SQLQueries.use_database(databaseName)

        #Grant the new user privileges on the new database
        query = SQLQ.SQLQueries.grant_access(databaseName, email)
        connection.execute_query(query)
        
        #Flush privileges
        query = SQLQ.SQLQueries.flush_privileges()
        connection.execute_query(query)
        
        #Add user details to the users database
        connection.execute_query(SQLQ.SQLQueries.use_users_database())

        connection.execute_query(SQLQ.SQLQueries.save_user_credentials(email, password, accountType, databaseName))
        
        connection.cnx.commit()
        
    except Exception as e:
        connection.close()
        print(f"Error: {e}")

    finally:
        connection.close()

        #innitializes the RapportMaker class
        RapportSetup = RM.RapportMaker()

        #Creates rapports for the new user and returns status information
        return {RapportSetup.createRapport(onlyEmail, "Disa"),
                RapportSetup.createRapport(onlyEmail, "Skrap"),
                RapportSetup.createRapport(onlyEmail, "Smelte"),
                RapportSetup.createRapport(onlyEmail, "Borreprove"),
                RapportSetup.createRapport(onlyEmail, "Sandanalyse")}

        



