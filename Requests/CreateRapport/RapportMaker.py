from SQLAdminConnections import SQL_AdminConnector as SQLC
from SQLAdminConnections import SQL_AdminQuerys as SQLQ


#class for creating rapports
class RapportMaker:
    def __init__(self):
        pass
    #Function for creating new rapport
    def createRapport(self, user_id, rapportType):
        if rapportType == "Disa":
            self.makeDisaRapport(user_id)
        elif rapportType == "Sandanalyse":
            self.makeSandanalyseRapport(user_id)
        elif rapportType == "Skrap":
            self.makeSkrapRapport(user_id)
        elif rapportType == "Smelte":
            self.makeSmelteRapport(user_id)
        elif rapportType == "Borreprove":
            self.makeBorreproveRapport(user_id)
        else:
            self.makeCustomRapport(user_id, rapportType)

    #Function for creating new disa rapport
    def makeDisaRapport(self, user_id):
        print("Making Disa rapport for " + str(user_id))
        return {"Status": "OK"}
    
    #Function for creating new sandanalyse rapport
    def makeSandanalyseRapport(self, user_id):
        print("Making Sandanalyse rapport for " + str(user_id))
    
    #Function for creating new skrap rapport
    def makeSkrapRapport(self, user_id):
        print("Making Skrap rapport for " + str(user_id))

    #Function for creating new smelte rapport
    def makeSmelteRapport(self, user_id):
        print("Making Smelte rapport for " + str(user_id))

    #Function for creating new borreprove rapport
    def makeBorreproveRapport(self, user_id):
        print("Making Borreprove rapport for " + str(user_id))

    
    #Function for creating new custom rapport
    def makeCustomRapport(self, user_id, jsonData):
        print("Making Custom rapport for " + str(user_id))
