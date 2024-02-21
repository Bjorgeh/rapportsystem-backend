from SQLAdminConnections import SQL_AdminConnector as SQLC
from SQLAdminConnections import SQL_AdminQuerys as SQLQ
from datetime import datetime, date, time, timedelta
from decimal import Decimal

class Data_insertor:
    def __init__(self):
        pass

    def insertData(self, email, table_name, data):
        try:
            # Changes @ and . in email to _
            email = email.replace("@", "_").replace(".", "_")

            # Connects to the database server
            connection = SQLC.SQLConAdmin()
            connection.connect()

            # Uses the database
            query = SQLQ.SQLQueries.use_database("DB_" + email)
            connection.execute_query(query)

            existing_tables = [table[0] for table in connection.execute_query(SQLQ.SQLQueries.show_tables())]
            if table_name not in existing_tables:
                raise Exception(f"Table {table_name} does not exist.")

            table_description = connection.execute_query(SQLQ.SQLQueries.getTableDescription(table_name))

            # Konverterer strenger til riktig datatype basert på tabellbeskrivelsen
            for column_info in table_description:
                column_name = column_info[0]
                column_type = column_info[1]
                if column_name in data:
                    if "int" in column_type:
                        data[column_name] = int(data[column_name])
                    elif "decimal" in column_type:
                        data[column_name] = Decimal(data[column_name])
                    elif "date" in column_type:
                        data[column_name] = datetime.strptime(data[column_name], "%Y-%m-%d").date()
                    elif "time" in column_type:
                        data[column_name] = datetime.strptime(data[column_name], "%H:%M:%S").time()
                    elif "datetime" in column_type:
                        data[column_name] = datetime.strptime(data[column_name], "%Y-%m-%d %H:%M:%S")

            # Setter inn data i tabellen
            insert_query = SQLQ.SQLQueries.insert_into_table(table_name, data)
            connection.execute_query(insert_query)
            connection.cnx.commit()

        except Exception as e:
            print(e)
            connection.cnx.close()
            connection.close()
            return {"Error": f"Error when inserting data into the table: {table_name}"}

        finally:
            connection.cnx.close()
            connection.close()
            return {"Success": f"Data inserted into the table: {table_name}"}