from SQLAdminConnections import SQL_AdminConnector as SQLC
from SQLAdminConnections import SQL_AdminQuerys as SQLQ
from flask_jwt_extended import jwt_required, get_jwt_identity

class data_extractor:
    def __init__(self):
        self.disaData = None
        self.skrapData = None
        self.smelteData = None
        self.borreproveData = None
        self.sandanalyseData = None
        
    def getDataFromTable(self,data):
        
        return {"Data": data},200

                    










                

