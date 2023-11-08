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
    def __init__(self,session):
        self.sesh_id = session

    def login(self):
        print("Login session function started:")
        # If there isn't a session_id, create one.
        if 'session_id' not in self.sesh_id:
            session_id = str(uuid.uuid4())
            self.sesh_id['session_id'] = session_id

            try:
                # Connect to the database and save the session_id for the user
                connection = SQLC.SQLConAdmin()
                connection.connect()
                print("Connected to SQL")

                # Execute queries to insert the session_id
                connection.execute_query(SQLQ.SQLQueries.use_users_database())
                connection.execute_query(SQLQ.SQLQueries.insert_session_id(self.sesh_id['session_id'], self.sesh_id['user_id']))
                print(SQLQ.SQLQueries.insert_session_id(self.sesh_id['session_id'], self.sesh_id['user_id']))
                connection.cnx.commit()

            except Exception as e:
                # Handle any exceptions that occur
                print(f"An error occurred during login: {e}")
                return False

            finally:
                # Ensure the connection is closed even if an error occurred
                if connection:
                    connection.close()
                print("Connection closed")

            return True

        # Session_id already exists
        print("ERROR: Session already exists.")
        return False
            
    def logout(self):
        # Check if session_id is present in the session data
        if 'session_id' in self.sesh_id:
            session_id = self.sesh_id['session_id']

            try:
                # Establish a connection to the database
                connection = SQLC.SQLConAdmin()
                connection.connect()

                # Execute queries to remove the session
                connection.execute_query(SQLQ.SQLQueries.use_users_database())
                connection.execute_query(SQLQ.SQLQueries.remove_session_id(session_id))
                connection.cnx.commit()

            except Exception as e:
                # Handle any exceptions that occur
                print(f"An error occurred while logging out: {e}")
                return False

            finally:
                # Ensure the connection is closed even if an error occurred
                if connection:
                    connection.close()

            # Session removal from the database was successful, proceed with local cleanup
            print(self.sesh_id, "Disconnected")

            # Remove session data from the local session storage
            for key in ['session_id', 'user_id', 'email', 'account_type']:
                self.sesh_id.pop(key, None)

            return True

        # No session_id found to remove
        return False

    def is_authenticated(self):
        #checks if 'session_id' is in the session data
        if 'session_id' not in self.sesh_id:
            return False

        #gets the session_id
        session_id = self.sesh_id['session_id']

        # Try to interact with the database
        try:
            # Create a connection to the database
            connection = SQLC.SQLConAdmin()
            connection.connect()

            # Select the correct database
            connection.execute_query(SQLQ.SQLQueries.use_users_database())

            # Check if the session has expired
            result = connection.execute_query(SQLQ.SQLQueries.check_session_expired(session_id))

        # Handle any exception that may occur during the database operations
        except Exception as e:
            print(f"An error occurred: {e}")
            return {'session_expired': True, 'message': 'Unable to verify session due to an error'}

        finally:
            # close the database connection
            connection.close()

        # Check the result of the session verification query
        if not result or result[0][0] != 1:
            print("Session not active or expired")
            #self.logout()
            return {'session_expired': True, 'message': 'Session not active or expired'}

        # If the session is still active, update the session's expiration
        self.update_session()
        return True
        
    def update_session(self):
        # Check for existence of 'session_id' in session
        if 'session_id' not in self.sesh_id:
            return False

        session_id = self.sesh_id['session_id']

        try:
            # Establish a connection to the database
            connection = SQLC.SQLConAdmin()
            connection.connect()

            # Execute queries to update session expiry
            connection.execute_query(SQLQ.SQLQueries.use_users_database())
            connection.execute_query(SQLQ.SQLQueries.update_session(session_id))
            connection.cnx.commit()

            # Close the connection to the database
            connection.close()
            return True

        except Exception as e:
            # Handle any exceptions that occur during the database operations
            print(f"An error occurred while updating the session: {e}")
            return False
    
    #Returns session_id
    def get_session_id(self):
        if 'session_id' not in self.sesh_id:
            return False

        return self.sesh_id['session_id']