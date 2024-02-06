from SQLAdminConnections import SQL_AdminConnector as SQLC
from SQLAdminConnections import SQL_AdminQuerys as SQLQ

#class for creating rapports
class RapportMaker:
    def __init__(self):
        self.newDisaRapport = ""
        self.newSandanalyseRapport = ""
        self.newSkrapRapport = ""
        self.newSmelteRapport = ""
        self.newBorreproveRapport = ""
        self.newCustomRapport = ""
        pass

    #Function for creating new rapport
    def createRapport(self, email, rapportType):
        if rapportType == "Disa":
            self.makeDisaRapport(email)
        elif rapportType == "Sandanalyse":
            self.makeSandanalyseRapport(email)
        elif rapportType == "Skrap":
            self.makeSkrapRapport(email)
        elif rapportType == "Smelte":
            self.makeSmelteRapport(email)
        elif rapportType == "Borreprove":
            self.makeBorreproveRapport(email)
        else:
            self.makeCustomRapport(email, rapportType)

    #Function for creating new disa rapport
    def makeDisaRapport(self, email):

        
        #sets up the name of the rapport
        self.newDisaRapport = "DisaRapport_"+str(email)

        '''
        #layout for DisaRapport
        #NAME: DisaRapport_[UserID]
        #RapportID(PRIM) INT | Shift VARCHAR | Time_and_date DATETIME | num_shaped INT | num_cast INT | Comment VARCHAR(255) | Model_tray INT
        '''

        #try to create the table for the rapport
        try:

            #Connection to the database
            adminConnection = SQLC.SQLConAdmin()

            #sets up connector with admin credentials
            connection = adminConnection
            connection.connect()

            #use the corrent database
            query = SQLQ.SQLQueries.use_database("DB_"+email)
            connection.execute_query(query)
            
            #Create the new table
            query = SQLQ.SQLQueries.create_table(self.newDisaRapport)
            connection.execute_query(query)

            #Add the columns to the table
            query = SQLQ.SQLQueries.insert_to_table(self.newDisaRapport, "rapportID", "INT", "PRIMARY KEY")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newDisaRapport, "shift", "VARCHAR(255)")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newDisaRapport, "time_and_date", "DATETIME")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newDisaRapport, "num_shaped", "INT")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newDisaRapport, "num_cast", "INT")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newDisaRapport, "comment", "VARCHAR(255)")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newDisaRapport, "model_tray", "INT")
            connection.execute_query(query)
            
            #commit the changes
            connection.cnx.commit()

        #returns error if any exception is raised
        except Exception as e:
            print("Error creating Disa rapport: " + str(e))
            connection.close()  #close the connection
            return {"Status": "Error", "Message": str(e)}, 500

        #return the name of the rapport
        print("Making Disa rapport for " + str(email))
        connection.close()  #close the connection
        return {"Rapport created": self.newDisaRapport, "Status": "Success", "Message": "Rapport created successfully"},200
    

    #Function for creating new sandanalyse rapport
    def makeSandanalyseRapport(self, email):
        '''
        #layout for sandanalyseRapport
        #NAME: sandanalyserapprot_[UserID]
        #ID(PRIM) INT | dato DATE | time TIME | fuktighet DECIMAL | Trykkstyrke DECIMAL | Pakningsgrad DECIMAL | Glødetap DECIMAL | Spaltestyrke DECIMAL | Aktiv_bentonitt DECIMAL
        | slam_innhold DECIMAL | sikteanalyse DECIMAL | sandanalysecol DECIMAL | kompersibilitet DECIMAL | sandtemperatur DECIMAL | signatur VARCHAR(20)
        '''
        #sets name of the rapport
        self.newSandanalyseRapport = "SandanalyseRapport_"+str(email)


        #try to create the table for the rapport
        try:
            #Connection to the database
            connection = SQLC.SQLConAdmin()
            connection = connection.connect()

            
            #use the corrent database
            query = SQLQ.SQLQueries.use_database("DB_"+email)
            connection.execute_query(query)

            #Create the new table
            query = SQLQ.SQLQueries.create_table(self.newSandanalyseRapport)
            connection.execute_query(query)

            #Add the columns to the table
            query = SQLQ.SQLQueries.insert_to_table(self.newSandanalyseRapport, "ID", "INT", "PRIMARY KEY")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newSandanalyseRapport, "dato", "DATE")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newSandanalyseRapport, "time", "TIME")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newSandanalyseRapport, "fuktighet", "DECIMAL")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newSandanalyseRapport, "Trykkstyrke", "DECIMAL")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newSandanalyseRapport, "Pakningsgrad", "DECIMAL")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newSandanalyseRapport, "Glødetap", "DECIMAL")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newSandanalyseRapport, "Spaltestyrke", "DECIMAL")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newSandanalyseRapport, "Aktiv_bentonitt", "DECIMAL")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newSandanalyseRapport, "slam_innhold", "DECIMAL")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newSandanalyseRapport, "sikteanalyse", "DECIMAL")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newSandanalyseRapport, "sandanalysecol", "DECIMAL")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newSandanalyseRapport, "kompersibilitet", "DECIMAL")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newSandanalyseRapport, "sandtemperatur", "DECIMAL")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newSandanalyseRapport, "signatur", "VARCHAR(20)")
            connection.execute_query(query)

            #commit the changes
            connection.cnx.commit()

        except Exception as e: 
            print("Error creating Sandanalyse rapport: " + str(e))
            connection.close()
            return {"Status": "Error", "Message": str(e)}, 500
        
        connection.close()
        return {"Rapport created": self.newSandanalyseRapport, "Status": "Success", "Message": "Rapport created successfully"},200
            
    
    #Function for creating new skrap rapport
    def makeSkrapRapport(self, email):
        '''
        #layout for skrapRapport
        #NAME: skraprapport_[UserID]
        #idSkrap(PRIM) INT | katalognummer INT | antall_bestilt INT | antall_manko INT | pris_pr_del FLOAT | sum_pris FLOAT | skrapcol VARCHAR(255)
        '''

        #sets name of the rapport
        self.newSkrapRapport = "SkrapRapport_"+str(email)

        #try to create the table for the rapport
        try:
            #Connection to the database
            connection = SQLC.SQLConAdmin()
            connection = connection.connect()

            
            #use the corrent database
            query = SQLQ.SQLQueries.use_database("DB_"+email)
            connection.execute_query(query)

            #Create the new table
            query = SQLQ.SQLQueries.create_table(self.newSkrapRapport)
            connection.execute_query(query)

            #Add the columns to the table
            query = SQLQ.SQLQueries.insert_to_table(self.newSkrapRapport, "idSkrap", "INT", "PRIMARY KEY")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newSkrapRapport, "katalognummer", "INT")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newSkrapRapport, "antall_bestilt", "INT")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newSkrapRapport, "antall_manko", "INT")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newSkrapRapport, "pris_pr_del", "FLOAT")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newSkrapRapport, "sum_pris", "FLOAT")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newSkrapRapport, "skrapcol", "VARCHAR(255)")
            connection.execute_query(query)

            #commit the changes
            connection.cnx.commit()

        except Exception as e:
            print("Error creating Skrap rapport: " + str(e))
            connection.close()
            return {"Status": "Error", "Message": str(e)}, 500
        
        connection.close()
        return {"Rapport created": self.newSkrapRapport, "Status": "Success", "Message": "Rapport created successfully"},200

    #Function for creating new smelte rapport
    def makeSmelteRapport(self, email):
        
        '''
        #layout for smelteRapport
        #NAME: smelterapport_[UserID]
        #registreringsID(PRIM) INT | ovnsnummer INT | dato DATE | tid TIME | kg_eget FLOAT | kg_stal FLOAT | totalvekt_smelte FLOAT | kg_karbon FLOAT | kg_malm FLOAT | 
        kg_fesi FLOAT | kg_fep FLOAT | kwh_for_smelte DOUBLE | kwh_etter_smelte DOUBLE | SUM_kwh_brukt DOUBLE 
        '''

        #sets name of the rapport
        self.newSmelteRapport = "SmelteRapport_"+str(email)

        #try to create the table for the rapport
        try:
            #Connection to the database
            connection = SQLC.SQLConAdmin()
            connection = connection.connect()

            #use the corrent database
            query = SQLQ.SQLQueries.use_database("DB_"+email)
            connection.execute_query(query)

            #Create the new table
            query = SQLQ.SQLQueries.create_table(self.newSmelteRapport)
            connection.execute_query(query)

            #Add the columns to the table
            query = SQLQ.SQLQueries.insert_to_table(self.newSmelteRapport, "registreringsID", "INT", "PRIMARY KEY")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newSmelteRapport, "ovnsnummer", "INT")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newSmelteRapport, "dato", "DATE")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newSmelteRapport, "tid", "TIME")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newSmelteRapport, "kg_eget", "FLOAT")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newSmelteRapport, "kg_stal", "FLOAT")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newSmelteRapport, "totalvekt_smelte", "FLOAT")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newSmelteRapport, "kg_karbon", "FLOAT")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newSmelteRapport, "kg_malm", "FLOAT")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newSmelteRapport, "kg_fesi", "FLOAT")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newSmelteRapport, "kg_fep", "FLOAT")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newSmelteRapport, "kwh_for_smelte", "DOUBLE")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newSmelteRapport, "kwh_etter_smelte", "DOUBLE")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newSmelteRapport, "SUM_kwh_brukt", "DOUBLE")
            connection.execute_query(query)

            #commit the changes
            connection.cnx.commit()

        except Exception as e:
            print("Error creating Smelte rapport: " + str(e))
            connection.close()
            return {"Status": "Error", "Message": str(e)}, 500
        
        connection.close()
        return {"Rapport created": self.newSmelteRapport, "Status": "Success", "Message": "Rapport created successfully"},200

    #Function for creating new borreprove rapport
    def makeBorreproveRapport(self, email):
        
        '''
        #layout for borreproveRapport
        #NAME: borreproverapport_[UserID]
        #proveID(PRIM) INT | deltype VARCHAR(45) | ovn VARCHAR(45) | katalognummer INT | antall_proveobjekter INT | ordrenummer VARCHAR(45) | godkjent TINYINT | dato DATE | tid TIME | signatur VARCHAR(45)
        '''

        #sets name of the rapport
        self.newBorreproveRapport = "BorreproveRapport_"+str(email)

        #try to create the table for the rapport
        try:
            #Connection to the database
            connection = SQLC.SQLConAdmin()
            connection = connection.connect()

            #use the corrent database
            query = SQLQ.SQLQueries.use_database("DB_"+email)
            connection.execute_query(query)

            #Create the new table
            query = SQLQ.SQLQueries.create_table(self.newBorreproveRapport)
            connection.execute_query(query)

            #Add the columns to the table
            query = SQLQ.SQLQueries.insert_to_table(self.newBorreproveRapport, "proveID", "INT", "PRIMARY KEY")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newBorreproveRapport, "deltype", "VARCHAR(45)")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newBorreproveRapport, "ovn", "VARCHAR(45)")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newBorreproveRapport, "katalognummer", "INT")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newBorreproveRapport, "antall_proveobjekter", "INT")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newBorreproveRapport, "ordrenummer", "VARCHAR(45)")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newBorreproveRapport, "godkjent", "TINYINT")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newBorreproveRapport, "dato", "DATE")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newBorreproveRapport, "tid", "TIME")
            connection.execute_query(query)
            query = SQLQ.SQLQueries.insert_to_table(self.newBorreproveRapport, "signatur", "VARCHAR(45)")
            connection.execute_query(query)

            #commit the changes
            connection.cnx.commit()

        except Exception as e:
            print("Error creating Borreprove rapport: " + str(e))
            connection.close()
            return {"Status": "Error", "Message": str(e)}, 500
        
        connection.close()
        return {"Rapport created": self.newBorreproveRapport, "Status": "Success", "Message": "Rapport created successfully"},200

    #Function for creating new custom rapport
    def makeCustomRapport(self, email, jsonData, dbname):
        '''
        #layout for customRapport
        #NAME: customrapport_[UserID]
        #ID(PRIM) INT | [custom data]
        '''
        #sets name of the rapport
        self.newCustomRapport = dbname+str(email)

        #try to create the table for the rapport
        try:
            #Connection to the database
            connection = SQLC.SQLConAdmin()
            connection = connection.connect()

            #use the corrent database
            query = SQLQ.SQLQueries.use_database("DB_"+email)
            connection.execute_query(query)

            #Create the new table
            query = SQLQ.SQLQueries.create_table(self.newCustomRapport)
            connection.execute_query(query)

            #Add the columns to the table
            query = SQLQ.SQLQueries.insert_to_table(self.newCustomRapport, "ID", "INT", "PRIMARY KEY")
            connection.execute_query(query)
            for key in jsonData:
                query = SQLQ.SQLQueries.insert_to_table(self.newCustomRapport, key, jsonData[key])
                connection.execute_query(query)

            #commit the changes
            connection.cnx.commit()

        except Exception as e:
            print("Error creating Custom rapport: " + str(e))
            connection.close()
            return {"Status": "Error", "Message": str(e)}, 500  
        
        connection.close()
        return {"Rapport created": self.newCustomRapport, "Status": "Success", "Message": "Rapport created successfully"},200
