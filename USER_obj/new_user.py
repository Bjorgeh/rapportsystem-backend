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
    def __init__(self, email, password, accountType):
        self.email = email
        self.password = password
        self.accountType = accountType
        self.databaseName = None

    #saves user to database
    def saveToDB(self):
        if self.accountType == "admin":
            save_admin.createNewAdminUser(self.email, self.password, self.accountType)
            print("Admin account created successfully")
            return True

        if self.accountType == 'leader':
            save_leader.createNewLeaderUser(self.email, self.password, self.accountType)
            print("Leader account created successfully")
            return True
        
        if self.accountType == 'operator':
            save_operator.createNewOperatorUser(self.email, self.password,self.accountType)
            print("Operator account created successfully")
            return True
        return False