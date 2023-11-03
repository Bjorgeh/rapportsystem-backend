class SQLQueries:
    #Belongs to the class, not the object of the class
    @staticmethod
    #Creates new database with given name
    def create_database(name):
        return f"CREATE DATABASE {name};"

    #Belongs to the class, not the object of the class
    @staticmethod
    #Creates new user with given name and password
    def create_user(usr, pw):
        return ("CREATE USER %s@'%' IDENTIFIED BY %s;", (usr, pw))

    #Belongs to the class, not the object of the class
    @staticmethod
    #grants privileges to user to its own database
    def grant_access(database,usr):
        return f"GRANT ALL PRIVILEGES ON {database}.* TO '{usr}'@'%';"
    
    #Belongs to the class, not the object of the class
    @staticmethod
    #Creates new database with given name
    def flush_privileges():
        return f"FLUSH PRIVILEGES;"
    
    #Belongs to the class, not the object of the class
    @staticmethod
    #Using the users database
    def use_users_database():
        return f"USE users;"

    #Belongs to the class, not the object of the class
    @staticmethod
    #saves user credentials to users database
    def save_user_credentials(email, password, accountType):
        return ("INSERT INTO user_info(email, userPass, accountType) VALUES (%s, %s, %s);", (email, password, accountType))
    
    #Belongs to the class, not the object of the class
    @staticmethod
    #Checks for invalid session timestamp
    def check_session_expired(session_id):
        return ("SELECT COUNT(*) FROM user_session "
                "WHERE CURRENT_TIMESTAMP > expiration AND session_id = %s",(session_id))