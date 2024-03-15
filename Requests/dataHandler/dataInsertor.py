from SQLAdminConnections import SQL_AdminConnector as SQLC
from SQLAdminConnections import SQL_AdminQuerys as SQLQ
from datetime import datetime, date, time, timedelta
from decimal import Decimal
from flask_jwt_extended import get_jwt_identity

#Class for inserting data into a table
class Data_insertor:
    def __init__(self, table_name, data): 
        self.current_user = get_jwt_identity()
        # Sets the username, key and database name
        self.username = self.current_user["email"]
        self.key = self.current_user["password"]
        self.db_name = self.current_user["db_name"]

        #Sets the table name and data
        self.table_name = table_name
        self.data = data

    def insertData(self):
        try:

            # Connects to the database server
            connection = SQLC.SQLConAdmin(None,self.username, self.key,self.db_name)
            connection.connect()

            # Uses the database
            query = SQLQ.SQLQueries.use_database(self.db_name)
            connection.execute_query(query)

            existing_tables = [table[0] for table in connection.execute_query(SQLQ.SQLQueries.show_tables())]
            if self.table_name not in existing_tables:
                raise Exception(f"Table {self.table_name} does not exist.")

            #Gets the table description
            table_description = connection.execute_query(SQLQ.SQLQueries.getTableDescription(self.table_name))

            #converts strings to the correct datatype based on the table description
            for column_info in table_description:
                column_name = column_info[0]
                column_type = column_info[1]
                if column_name in self.data:
                    if "int" in column_type:
                        self.data[column_name] = int(self.data[column_name])
                    elif "decimal" in column_type:
                        self.data[column_name] = Decimal(self.data[column_name])
                    elif "date" in column_type:
                        self.data[column_name] = datetime.strptime(self.data[column_name], "%Y-%m-%d").date()
                    elif "time" in column_type:
                        self.data[column_name] = datetime.strptime(self.data[column_name], "%H:%M:%S").time()
                    elif "datetime" in column_type:
                        self.data[column_name] = datetime.strptime(self.data[column_name], "%Y-%m-%d %H:%M:%S")

            #Sets data into the table
            insert_query = SQLQ.SQLQueries.insert_into_table(self.table_name, self.data)
            connection.execute_query(insert_query)
            connection.cnx.commit()

        except Exception as e:
            print(e)
            connection.cnx.close()
            connection.close()
            return {"Error": f"Error when inserting data into the table: {self.table_name}"}

        finally:
            connection.cnx.close()
            connection.close()
            return {"Success": f"Data inserted into the table: {self.table_name}"}