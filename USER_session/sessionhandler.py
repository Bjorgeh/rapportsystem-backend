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
    def __init__(self, session):
        self.session = session  # Flask-Session object

    #Creates new session and logs in user
    def login(self):
        print("Login session function started:")
        user_id = self.session.get('user_id')

        # Slett eksisterende sessions for denne brukeren
        self.delete_old_user_sessions(user_id)

        # Opprett ny session
        session_id = self.session.sid
        try:
            connection = SQLC.SQLConAdmin()
            connection.connect()
            print("Connected to SQL")
            connection.execute_query(SQLQ.SQLQueries.use_users_database())
            connection.execute_query(SQLQ.SQLQueries.insert_session_id(session_id, user_id))
            connection.cnx.commit()
        except Exception as e:
            print(f"An error occurred during login: {e}")
            return False
        finally:
            if connection:
                connection.close()
            print("Connection closed")
        return True

    #Logs out user
    def logout(self):
        session_id = self.session.sid  
        if session_id:
            try:
                connection = SQLC.SQLConAdmin()
                connection.connect()
                connection.execute_query(SQLQ.SQLQueries.use_users_database())
                connection.execute_query(SQLQ.SQLQueries.remove_session_id(session_id))
                #connection.execute_query(SQLQ.SQLQueries.remove_session_id(self.session.get('user_id')))
                connection.cnx.commit()
            except Exception as e:
                print(f"An error occurred while logging out: {e}")
                return False
            finally:
                if connection:
                    connection.close()
            print(self.session, "Disconnected")
            self.session.clear()  #removes all session data
            return True
        return False

    #Checks if session is authenticated - Should only return true/false
    def is_authenticated(self):
        session_id = self.session.sid

        if not session_id:
            return False

        try:
            connection = SQLC.SQLConAdmin()
            connection.connect()
            connection.execute_query(SQLQ.SQLQueries.use_users_database())

            #Checks if session is expired
            expiration_result = connection.execute_query(SQLQ.SQLQueries.check_session_expired(self.session.get('user_id')))
            if not expiration_result or expiration_result[0][0] != 0:
                print("Session expired based on expiration timestamp")
                #return False
                return {"AUTH": False, "Reason": "Session expired"}

            #checks if session in database is active
            active_session_result = connection.execute_query(SQLQ.SQLQueries.get_active_session(self.session.get('user_id')))
            if not active_session_result:
                print("No active session found")
                #return False
                return {"AUTH": False, "Reason": "No active session"}
            db_session_id = active_session_result[0][0]  
            
            #checks if session-ID matches the one in the database
            if db_session_id != session_id:
                print("Session ID mismatch")
                #return False
                return {"AUTH": False, "Reason": "Logged in from another device."}

        except Exception as e:
            print(f"An error occurred: {e}")
            #return False
            return {"AUTH": False, "Reason": "Unable to verify session due to an internal SQL error"}
        finally:
            connection.close()

        return {"AUTH":True}
        
    #Updates session
    def update_session(self):
        session_id = self.session.sid

        if not session_id:
            return False
 
        try:
            connection = SQLC.SQLConAdmin()
            connection.connect()
            connection.execute_query(SQLQ.SQLQueries.use_users_database())
            connection.execute_query(SQLQ.SQLQueries.update_session(session_id))
            connection.cnx.commit()
        except Exception as e:
            print(f"An error occurred while updating the session: {e}")
            return False
        finally:
            connection.close()
    
        return True
    
    #Returns session_id
    def get_session_id(self):
        return self.session.sid if 'sid' in self.session else None
    

    #fiction for removing old sessions
    def delete_old_user_sessions(self, user_id):
    
        try:
            connection = SQLC.SQLConAdmin()
            connection.connect()  
            query, params = SQLQ.SQLQueries.delete_old_sessions_by_user_id(user_id)

            connection.execute_query(SQLQ.SQLQueries.use_users_database())
            connection.execute_query((query, params))
            connection.cnx.commit()  
            rows_affected = connection.cursor.rowcount
            print(f"Deleted {rows_affected} sessions for user_id {user_id}.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            connection.close()