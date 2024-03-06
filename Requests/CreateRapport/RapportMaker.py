from SQLAdminConnections import SQL_AdminConnector as SQLC
from SQLAdminConnections import SQL_AdminQuerys as SQLQ

#class for creating rapports
class RapportMaker:
    def __init__(self):
        self.newDisaRapport = "DisaRapport_"
        self.newSandanalyseRapport = "SandanalyseRapport"
        self.newSkrapRapport = "SkrapRapport"
        self.newSmelteRapport = "SmalteRapport"
        self.newBorreproveRapport = "BorreproveRapport"
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

        databaseName = "db_"+email.replace("@", "_").replace(".", "_")
        onlyEmail = email.replace("@", "_").replace(".", "_")

        #sets up the name of the rapport
        self.newDisaRapport = "DisaRapport_"+str(onlyEmail)

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
            query = SQLQ.SQLQueries.use_database(databaseName)
            print(query)
            connection.execute_query(query)
            
            
            #Create the new table
            query = SQLQ.SQLQueries.create_disa_table(self.newDisaRapport)
            print(query)
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

        databaseName = "db_"+email.replace("@", "_").replace(".", "_")
        onlyEmail = email.replace("@", "_").replace(".", "_")
        '''
        #layout for sandanalyseRapport
        #NAME: sandanalyserapprot_[UserID]
        #ID(PRIM) INT | dato DATE | time TIME | fuktighet DECIMAL | Trykkstyrke DECIMAL | Pakningsgrad DECIMAL | Glødetap DECIMAL | Spaltestyrke DECIMAL | Aktiv_bentonitt DECIMAL
        | slam_innhold DECIMAL | sikteanalyse DECIMAL | sandanalysecol DECIMAL | kompersibilitet DECIMAL | sandtemperatur DECIMAL | signatur VARCHAR(20)
        '''
        #sets name of the rapport
        self.newSandanalyseRapport = "SandanalyseRapport_"+str(onlyEmail)

        #try to create the table for the rapport
        try:
            #Connection to the database
            connection = SQLC.SQLConAdmin()
            connection.connect()

            
            #use the corrent database
            query = SQLQ.SQLQueries.use_database(databaseName)
            connection.execute_query(query)

            #Create the new table
            query = SQLQ.SQLQueries.create_sandAnalyseRapport_table(self.newSandanalyseRapport)
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
        databaseName = "db_"+email.replace("@", "_").replace(".", "_")
        onlyEmail = email.replace("@", "_").replace(".", "_")
        '''
        #layout for skrapRapport
        #NAME: skraprapport_[UserID]
        #idSkrap(PRIM) INT | katalognummer INT | antall_bestilt INT | antall_manko INT | pris_pr_del FLOAT | sum_pris FLOAT | skrapcol VARCHAR(255)
        '''

        #sets name of the rapport
        self.newSkrapRapport = "SkrapRapport_"+str(onlyEmail)

        #try to create the table for the rapport
        try:
            #Connection to the database
            connection = SQLC.SQLConAdmin()
            connection.connect()

            #use the corrent database
            query = SQLQ.SQLQueries.use_database(databaseName)
            connection.execute_query(query)

            #Create the new table
            query = SQLQ.SQLQueries.create_skrapRapport_table(self.newSkrapRapport)
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
        databaseName = "db_"+email.replace("@", "_").replace(".", "_")
        onlyEmail = email.replace("@", "_").replace(".", "_")
        
        '''
        #layout for smelteRapport
        #NAME: smelterapport_[UserID]
        #registreringsID(PRIM) INT | ovnsnummer INT | dato DATE | tid TIME | kg_eget FLOAT | kg_stal FLOAT | totalvekt_smelte FLOAT | kg_karbon FLOAT | kg_malm FLOAT | 
        kg_fesi FLOAT | kg_fep FLOAT | kwh_for_smelte DOUBLE | kwh_etter_smelte DOUBLE | SUM_kwh_brukt DOUBLE 
        '''

        #sets name of the rapport
        self.newSmelteRapport = "SmelteRapport_"+str(onlyEmail)

        #try to create the table for the rapport
        try:
            #Connection to the database
            connection = SQLC.SQLConAdmin()
            connection.connect()

            #use the corrent database
            query = SQLQ.SQLQueries.use_database(databaseName)
            connection.execute_query(query)

            #Create the new table
            query = SQLQ.SQLQueries.create_smelteRapport_table(self.newSmelteRapport)
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
        databaseName = "db_"+email.replace("@", "_").replace(".", "_")
        onlyEmail = email.replace("@", "_").replace(".", "_")
        
        '''
        #layout for borreproveRapport
        #NAME: borreproverapport_[UserID]
        #proveID(PRIM) INT | deltype VARCHAR(45) | ovn VARCHAR(45) | katalognummer INT | antall_proveobjekter INT | ordrenummer VARCHAR(45) | godkjent TINYINT | dato DATE | tid TIME | signatur VARCHAR(45)
        '''

        #sets name of the rapport
        self.newBorreproveRapport = "BorreproveRapport_"+str(onlyEmail)

        #try to create the table for the rapport
        try:
            #Connection to the database
            connection = SQLC.SQLConAdmin()
            connection.connect()

            #use the corrent database
            query = SQLQ.SQLQueries.use_database(databaseName)
            connection.execute_query(query)

            #Create the new table
            query = SQLQ.SQLQueries.create_borreproverapport_table(self.newBorreproveRapport)
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
        databaseName = "db_"+email.replace("@", "_").replace(".", "_")
        onlyEmail = email.replace("@", "_").replace(".", "_")
        '''
        #layout for customRapport
        #NAME: customrapport_[UserID]
        #ID(PRIM) INT | [custom data]
        '''
        #sets name of the rapport
        self.newCustomRapport = dbname+str(onlyEmail)

        #try to create the table for the rapport
        try:
            #Connection to the database
            connection = SQLC.SQLConAdmin()
            connection.connect()

            #use the corrent database
            query = SQLQ.SQLQueries.use_database(databaseName)
            connection.execute_query(query)

            #Create the new table
            query = SQLQ.SQLQueries.create_table(self.newCustomRapport)
            connection.execute_query(query)

            #Add the columns to the table
            query = SQLQ.SQLQueries.add_column(self.newCustomRapport, "ID", "INT", "PRIMARY KEY")
            connection.execute_query(query)
            for key in jsonData:
                query = SQLQ.SQLQueries.add_column(self.newCustomRapport, key, jsonData[key])
                connection.execute_query(query)

            #commit the changes
            connection.cnx.commit()

        except Exception as e:
            print("Error creating Custom rapport: " + str(e))
            connection.close()
            return {"Status": "Error", "Message": str(e)}, 500  
        
        connection.close()
        return {"Rapport created": self.newCustomRapport, "Status": "Success", "Message": "Rapport created successfully"},200
