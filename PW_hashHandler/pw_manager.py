import bcrypt

#Defines the PasswordManager class
class PwManager:
    def __init__(self):
        pass
    
     #Hashes a plain password and return its hashed value.
    def encrypt_pw(self, plaintext_pw: str) -> bytes:

        #convert the plaintext password string to bytes
        password_bytes = plaintext_pw.encode('utf-8')
        
        #Hashes the password
        hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        return hashed_password

    #checks if password is correct
    def check_pw(self, plaintext_pw: str, stored_hashed_password: bytes) -> bool:
        #Check if a password matches the hashed password
        # Convert the plaintext password string to bytes
        password_bytes = plaintext_pw.encode('utf-8')
        
        # Verify the password
        return bcrypt.checkpw(password_bytes, stored_hashed_password)




#defines hash, takes password and returns hashed password
def hash(password):
    password_manager = PwManager()
    hashed_pw = password_manager.encrypt_pw(password)
    return hashed_pw

#defines check, takes password and hashed password and returns true/false
def check(password, hashed_pw):
    password_manager = PwManager()
    is_password_correct = password_manager.check_pw(password, hashed_pw)
    return is_password_correct