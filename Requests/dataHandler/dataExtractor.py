from SQLAdminConnections import SQL_AdminConnector as SQLC
from SQLAdminConnections import SQL_AdminQuerys as SQLQ
from datetime import datetime, date, time, timedelta
from decimal import Decimal

from flask_jwt_extended import get_jwt_identity

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
            query = SQLQ.SQLQueries.use_database("db_" + email)
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
            query = SQLQ.SQLQueries.use_database("db_" + email)
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

    def _parse_date(self, date_str):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return None

    def extractGivenTable(self, email, table_name, start_date=None, stop_date=None, num_rows=None):
        connection = None  # Initialize connection variable to None
        try:
            dbName= email.replace("@", "_").replace(".", "_")
            result_dict = {}

            userDatabaseLogin = get_jwt_identity()

            # Define connection variable first            
            connection = SQLC.SQLConAdmin(None, userDatabaseLogin['email'], userDatabaseLogin['password'], userDatabaseLogin['db_name'])
            connection.connect()
            print("Connected to the database")

            # Use the specified database
            use_database_query = SQLQ.SQLQueries.use_database(self.getDatabaseName(email))
            connection.execute_query(use_database_query)

            # Get the data from the table
            query = SQLQ.SQLQueries.getAllFromTable(table_name)
            if start_date and stop_date:
                # Konverter start_date og stop_date til datetime-objekter
                start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
                stop_datetime = datetime.strptime(stop_date, '%Y-%m-%d')
                query = SQLQ.SQLQueries.get_data_between_dates(table_name, start_datetime, stop_datetime)
            # If num_rows is provided, get the first num_rows rows from the table
            elif num_rows:
                query = SQLQ.SQLQueries.limit_query(table_name, num_rows)

            # Get the data from the table
            data_in_table = connection.execute_query(query)

            # Get the table description
            table_description = connection.execute_query(SQLQ.SQLQueries.getTableDescription(table_name))
            table_description = {col[0]: str(col[1]) if isinstance(col[1], (datetime, date, time, timedelta, Decimal)) else col[1] for col in table_description}

            # Convert datetime objects to strings in the data
            data_in_table = [dict(zip(table_description.keys(), (str(value) if isinstance(value, (datetime, date, time, timedelta, Decimal)) else value for value in row))) for row in data_in_table]

            # Add the data to the dictionary
            result_dict[table_name] = {"Data": data_in_table}

        except Exception as e:
            # Log the exception for better error tracking
            print(e)
            return {"Error": f"Error when extracting data from the database for table: {table_name}"}

        finally:
            # Close the connection if it's not None
            if connection:
                print("Closing the connection")
                connection.cnx.close()
                connection.close()

        return {"requested_data": result_dict}

    # Extracts the database name from the user
    def getDatabaseName(self,email):
        try:
            connection = SQLC.SQLConAdmin()
            connection.connect()

            #Uses the database
            query = SQLQ.SQLQueries.use_users_database()
            connection.execute_query(query)

            #Gets the database name from the email
            query = SQLQ.SQLQueries.get_database_name(email)
            dbName = connection.execute_query(query)
            userDataBaseName = dbName[0][0]
            connection.cnx.close()
            connection.close()

        except Exception as e:
            print(e)
            connection.cnx.close()
            connection.close()
            return {"Error": "Error when extracting database name from the database for user: " + email}
        
        finally:
            connection.cnx.close()
            connection.close()

            return userDataBaseName