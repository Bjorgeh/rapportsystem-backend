from SQLAdminConnections import SQL_AdminConnector as SQLC
from SQLAdminConnections import SQL_AdminQuerys as SQLQ
from datetime import datetime, date, time, timedelta
from decimal import Decimal

from flask_jwt_extended import get_jwt_identity

#Defines the class data_extractor
class table_info_extractor:
    def __init__(self):
        pass

    def extractTableDescription(self):
        try:
            #changes @ and . in email to _
            current_user = get_jwt_identity()
            key = current_user["password"]
            dbName = current_user["db_name"]
            username = current_user["email"]

            #Dict for storing data
            result_dict = {}

            #Connects to the database server
            connection = SQLC.SQLConAdmin(None,username,key,dbName)
            connection.connect()

            #Uses the database
            query = SQLQ.SQLQueries.use_database(dbName)
            connection.execute_query(query)

            #Gets all tablenames from the database
            show_tables_query = SQLQ.SQLQueries.show_tables()
            all_tables = connection.execute_query(show_tables_query)

            #Gets tablenames and description from the database
            for table in all_tables:
                #Gets the current table
                current_table = table[0]

                #Adds the data to the dictionary
                table_description = connection.execute_query(SQLQ.SQLQueries.getTableDescription(current_table))
                
                #Convert datetime objects to strings in the description
                table_description = {col[0]: str(col[1]) if isinstance(col[1], (datetime, date, time, timedelta, Decimal)) else col[1] for col in table_description}

                #Adds the data to the dictionary
                result_dict[current_table] = table_description

        # Error handling
        except Exception as e:
            print(e)
            connection.cnx.close()
            connection.close()
            return {"Error": "Error when extracting table description from the database for table: " + current_table}
        
        # Returns closes the connection and returns the data
        finally:
            connection.cnx.close()
            connection.close()
            return {"Tables": result_dict}