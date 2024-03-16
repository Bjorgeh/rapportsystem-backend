from SQLAdminConnections import SQL_AdminConnector as SQLC
from SQLAdminConnections import SQL_AdminQuerys as SQLQ
from datetime import datetime,date,time
from decimal import Decimal
from flask_jwt_extended import get_jwt_identity

class data_changer:
    def __init__(self, table_name, data = None): 
        self.current_user = get_jwt_identity()
        # Sets the username, key and database name
        self.username = self.current_user["email"]
        self.key = self.current_user["password"]
        self.db_name = self.current_user["db_name"]

        # Sets the table name and data
        self.table_name = table_name
        self.data = data

    def changeData(self):
        try:
            # Connects to the database server
            connection = SQLC.SQLConAdmin(None, self.username, self.key, self.db_name)
            connection.connect()

            # Uses the database
            query = SQLQ.SQLQueries.use_database(self.db_name)
            connection.execute_query(query)

            # Checks if the table exists
            existing_tables = [table[0] for table in connection.execute_query(SQLQ.SQLQueries.show_tables())]
            if self.table_name not in existing_tables:
                raise Exception(f"Table {self.table_name} does not exist.")

            # Gets the table description
            table_description = connection.execute_query(SQLQ.SQLQueries.getTableDescription(self.table_name))

            # Converts strings to the correct datatype based on the table description
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

            # Update the last row with new data based on the latest "id"
            update_query = SQLQ.SQLQueries.update_last_row_by_id(self.table_name, self.data)
            connection.execute_query(update_query)
            connection.cnx.commit()

        except Exception as e:
            print(e)
            connection.cnx.rollback()  # Rollback changes if an error occurs
            return {"Error": f"Error when updating data in the table: {self.table_name}"}

        finally:
            connection.cnx.close()
            connection.close()
            return {"Success": f"Data updated in the table: {self.table_name}"}

    def deleteLastRow(self):
        try:
            # Connects to the database server
            connection = SQLC.SQLConAdmin(None, self.username, self.key, self.db_name)
            connection.connect()

            # Uses the database
            query = SQLQ.SQLQueries.use_database(self.db_name)
            connection.execute_query(query)

            # Checks if the table exists
            existing_tables = [table[0] for table in connection.execute_query(SQLQ.SQLQueries.show_tables())]
            if self.table_name not in existing_tables:
                raise Exception(f"Table {self.table_name} does not exist.")

            # Deletes the last row from the table based on the latest "id"
            delete_query = SQLQ.SQLQueries.delete_last_row_by_id(self.table_name)
            connection.execute_query(delete_query)
            connection.cnx.commit()

        except Exception as e:
            print(e)
            connection.cnx.rollback()  # Rollback changes if an error occurs
            return {"Error": f"Error when deleting last row from the table: {self.table_name}"}

        finally:
            connection.cnx.close()
            connection.close()
            return {"Success": f"Last row deleted from the table: {self.table_name}"}

