import os
#Gets current directory
current_directory = os.getcwd()
#imports sys
import sys
sys.path.append(os.path.join(current_directory))

#Imports SQLAdminConnections modules
from SQLAdminConnections import SQL_CreateNewLeaderUser as save_leader
from SQLAdminConnections import SQL_CreateNewOperatorUser as save_operator
from SQLAdminConnections import SQL_CreateNewAdminUser as save_admin

#Takes in user object and saves it to database
class createUser:
    def __init__(self, email, password, key):
        self.email = email
        self.password = password
        self.accountType = "admin"
        self.databaseName = None
        self.key = key

    #saves user to database
    def saveToDB(self):
        if self.accountType == "admin":
            save_admin.createNewAdminUser(self.email, self.password, self.accountType, self.key)
            print("Admin account created successfully")
            return True
    
        else:
            return False