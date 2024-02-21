from SQLAdminConnections import SQL_AdminConnector as SQLC
from SQLAdminConnections import SQL_AdminQuerys as SQLQ
from datetime import datetime, date, time, timedelta
from decimal import Decimal

#Defines the class data_extractor
class data_extractor:
    def __init__(self):
        pass

    def extractTableDescription(self, email):
        try:
            #changes @ and . in email to _
            email = email.replace("@", "_").replace(".", "_")

            #Dict for storing data
            result_dict = {}

            #Connects to the database server
            connection = SQLC.SQLConAdmin()
            connection.connect()

            #Uses the database
            query = SQLQ.SQLQueries.use_database("DB_" + email)
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

    # Gets data from the database
    def extractData(self, email):
        try:
            #changes @ and . in email to _
            email = email.replace("@", "_").replace(".", "_")

            #Dict for storing data
            result_dict = {}

            #Connects to the database server
            connection = SQLC.SQLConAdmin()
            connection.connect()

            #Uses the database
            query = SQLQ.SQLQueries.use_database("DB_" + email)
            connection.execute_query(query)

            #Gets all tablenames from the database
            show_tables_query = SQLQ.SQLQueries.show_tables()
            all_tables = connection.execute_query(show_tables_query)

            #Gets tablenames and data from the database
            for table in all_tables:
                #Gets the current table
                current_table = table[0]

                #Adds the data to the dictionary
                table_description = connection.execute_query(SQLQ.SQLQueries.getTableDescription(current_table))
                
                #Convert datetime objects to strings in the description
                table_description = {col[0]: str(col[1]) if isinstance(col[1], (datetime, date, time, timedelta, Decimal)) else col[1] for col in table_description}

                #Gets all data from current table
                data_in_tables = connection.execute_query(SQLQ.SQLQueries.getAllFromTable(current_table))

                #Convert datetime objects to strings in the data
                data_in_tables = [dict(zip(table_description.keys(), (str(value) if isinstance(value, (datetime, date, time, timedelta, Decimal)) else value for value in row))) for row in data_in_tables]

                #Adds the data to the dictionary
                result_dict[current_table] = {"Table_description": table_description, "Data": data_in_tables}

        # Error handling
        except Exception as e:
            print(e)
            connection.cnx.close()
            connection.close()
            return {"Error": "Error when extracting data from the database for table: " + current_table}
        
        # Returns closes the connection and returns the data
        finally:
            connection.cnx.close()
            connection.close()
            return {"Tables": result_dict}        

                    










                

