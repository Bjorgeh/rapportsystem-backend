import os
#Gets current directory
current_directory = os.getcwd()
#imports sys
import sys
sys.path.append(os.path.join(current_directory))

#Imports SQLAdminConnections modules
from SQLAdminConnections import SQL_AdminConnector as SQLC
from SQLAdminConnections import SQL_AdminQuerys as SQLQ

#user class for handeling user data
class users:
    def __init__(self,ID=None,email=None,password=None,accountType=None,databaseName=None, session_id=None):
        self.userID = ID
        self.email = email
        self.password = password
        self.databaseName = databaseName
        self.accountType = accountType
        self.sessionID = session_id

    #updates user ID
    def updateID(self,ID):
        if not ID:
            return 'ID not updated'

        self.userID = ID
        return 'ID updated:', ID

    #updates user email
    def updateEmail(self,email):
        if not email:
            return 'Email not updated'

        self.email = email
        return 'new email:' + email
    
    #updates user password
    def updatePassword(self,password):
        if not password:
            return 'Password not updated'

        self.password = password
        return 'Password updated!'
    
    #updates user database name
    def updateDatabaseName(self,databaseName):
        if not databaseName:
            return 'Database name not updated'
        self.databaseName = databaseName
        return 'Database name updated:' + databaseName
    
    #updates user account type
    def updateAccountType(self,accountType):
        if not accountType:
            return 'Account type not updated'
        self.accountType = accountType
        return 'Account type updated:' + accountType
    
    def updatesessionId(self, session_id):
        if not session_id:
            return 'Session ID not updated'
        self.sessionID = session_id
        return 'Session ID updated:' + session_id
    
    #returns user email
    def getEmail(self):
        if not self.email:
            return 'No email found'
        return self.email
    
    #returns user password
    def getPassword(self):
        if not self.password:
            return 'Password is protected'
        return self.password
    
    #returns user database name
    def getDatabaseName(self):
        if not self.databaseName:
            return 'No database name found'
        return self.databaseName
    
    #returns user account type
    def getAccountType(self):
        if not self.accountType:
            return 'No account type found'
        return self.accountType
    
    #returns user session ID
    def getSessionID(self):
        if not self.sessionID:
            return 'No sessionID type found'
        return self.sessionID
    
    #returns user ID
    def getID(self):
        if not self.userID:
            return 'No ID found'
        return self.userID
    
    #Returns true if leader, else false
    def isLeader(self):
        return self.accountType == 'leader'
    #returns true if operator, else false
    def isOperator(self):
        return self.accountType == 'operator'
    #returns true if admin, else false
    def isAdmin(self):
        return self.accountType == 'admin'

    #returns true if session expired, else false
    def isSessionExpired(self):
        return self.internalSC(self.sessionID)    

    #retuns true if session expired, else false SC = sessioncheck
    def internalSC(session_id):

        #connect to database
        connection = SQLC.SQLConAdmin()

        #Execute query
        connection.execute_query(SQLQ.SQLQueries.check_session_expired(session_id))
        
        #get result
        (count,) = connection.cursor.fetchone()

        #close connection
        connection.close()

        #returns true if session is expired, else false
        return count > 0
