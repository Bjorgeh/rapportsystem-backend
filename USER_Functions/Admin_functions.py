class admin_functions:
    def __init__(self, userObjekt):
        self.id = userObjekt.getID()
        self.email = userObjekt.getEmail() 
        self.accountType = userObjekt.getAccountType()

    #Sets new password for user
    def Support_updatePassword(self,email,new_password1, new_password2):
        if not new_password1 == new_password2:
            return {"Password": "Does not match."}
        
        if not email == "EMAIL FROM DATABASE":
            return {"Email": "Not found."}
            
        #Update a users password here.
        
        return {"Passwrod": "Updated!", "New password": "PROTECTED"}
    
    #Sets new email for user
    def Support_updateEmail(self,new_email1, new_email2):
        if not new_email1 == new_email2:
            return {"Email": "Does not match."}
        
        #Update a users email here.

        return {"Email": "Updated!", "New email": new_email1}