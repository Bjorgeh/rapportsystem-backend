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
class createSubUser:
    def __init__(self, email, password, accountType, creatorAccount,key,rapportName = None):
        self.email = email
        self.password = password
        self.accountType = accountType
        self.creatorAccount = creatorAccount
        self.rapportName = rapportName
        self.key = key

    #saves user to database
    def saveToDB(self):
        if self.accountType == "admin":
            #save_admin.createNewAdminUser(self.email, self.password, self.accountType) < dont use this

            '''Could add functuinallity to allow admin to create SUB admin accounts'''
            #save_subadmin.createNewSubAdminUser(self.email, self.password, self.accountType)

            print("Admin can't create admin account.") 
            return False

        if self.accountType == 'leader':
            save_leader.createNewLeaderUser(self.email, self.password, self.accountType, self.creatorAccount, self.key)
            print("Leader account created successfully")
            return True
        
        if self.accountType == 'operator':
            save_operator.createNewOperatorUser(self.email, self.password,self.accountType,self.creatorAccount, self.key, self.rapportName)
            print("Operator account created successfully")
            return True
        return False