import uuid
#imports os
import os
current_directory = os.getcwd()
#imports sys
import sys
sys.path.append(os.path.join(current_directory))

from SQLAdminConnections import SQL_AdminConnector as SQLC
from SQLAdminConnections import SQL_AdminQuerys as SQLQ

class UserSession:
    def __init__(self,session, user_id):
        self.sesh_id = session
        self.user_id = user_id

    def login(self):
        # If there isn't a session_id, create one.
        if 'session_id' not in self.sesh_id:
            session_id = str(uuid.uuid4())
            self.sesh_id['session_id'] = session_id

            # Connect to the database and save the session_id for the user
            connection = SQLC.SQLConAdmin()
            connection.connect()
            print("Connected to SQL")
            connection.execute_query(SQLQ.SQLQueries.use_users_database())
            connection.execute_query(SQLQ.SQLQueries.insert_session_id(self.sesh_id['session_id'], self.user_id))
            print("Query sendt to database")
            connection.cnx.commit()
            connection.close()
            print("Connection closed")
            

    def logout(self):
        # Remove the session from the database if exists
        if 'session_id' in self.sesh_id:
            session_id = self.sesh_id['session_id']

            connection = SQLC.SQLConAdmin()
            connection.connect()
            connection.execute_query(SQLQ.SQLQueries.use_users_database())
            connection.execute_query(SQLQ.SQLQueries.remove_session_id(session_id))
            connection.cnx.commit()
            connection.close()
            
            print(self.sesh_id +"Disconnected")
            # Remove the session_id from Flask's session
            del self.sesh_id['session_id']

    def is_authenticated(self):
        if 'session_id' not in self.sesh_id:
            return False

        session_id = self.sesh_id['session_id']
        connection = SQLC.SQLConAdmin()
        connection.connect()
        connection.execute_query(SQLQ.SQLQueries.get_active_session(session_id))
        status = connection.cursor.fetchone() 
        connection.close()

        return bool(status)