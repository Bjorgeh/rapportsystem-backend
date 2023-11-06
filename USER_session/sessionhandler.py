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
        print("Login session function started:")
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
            print(SQLQ.SQLQueries.insert_session_id(self.sesh_id['session_id'], self.user_id))
            connection.cnx.commit()
            connection.close()
            print("Connection closed")

            return True
        print("ERROR making new session")
        return False
            
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
            
            print(self.sesh_id,"Disconnected")
            
            #Remove the session_id from Flask's session
            del self.sesh_id['session_id']

    def is_authenticated(self):
        if 'session_id' not in self.sesh_id:
            return False

        session_id = self.sesh_id['session_id']
        connection = SQLC.SQLConAdmin()
        connection.connect()
        connection.execute_query(SQLQ.SQLQueries.use_users_database())
        #connection.execute_query(SQLQ.SQLQueries.check_session_expired(session_id))
        result = connection.execute_query(SQLQ.SQLQueries.check_session_expired(session_id))
        connection.close()

        print(result)
                
        # If the session has expired, return False
        if result is not None and result[0][0] == 1:
            print("Session expired")
            self.logout()
            return {'session_expired': True, 'message': 'Session expired'}
                
        # If the session hasn't expired, return True
        self.update_session()
        return True

    #Updates expiration with extra 30 minutes.
    def update_session(self):

        if 'session_id' not in self.sesh_id:
            return False

        session_id = self.sesh_id['session_id']
        connection = SQLC.SQLConAdmin()
        connection.connect()
        connection.execute_query(SQLQ.SQLQueries.use_users_database())
        #connection.execute_query(SQLQ.SQLQueries.update_users_database())
        connection.execute_query(SQLQ.SQLQueries.update_session(session_id))
        connection.cnx.commit()
        connection.close()

        return True