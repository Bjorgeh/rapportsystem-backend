import uuid
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt

from SQLAdminConnections import SQL_AdminConnector as SQLC
from SQLAdminConnections import SQL_AdminQuerys as SQLQ

class UserTokenHandler:
    def __init__(self):
        pass

    # Generates a JWT for a given user
    def login(self, user_id):
        additional_claims = {"user_id": user_id}
        access_token = create_access_token(identity=user_id, additional_claims=additional_claims)
        jti = get_jwt()["jti"]  # Extracting the JTI from the token
        self.store_token(user_id, jti)  # Storing the token's JTI in the database
        return access_token

    # Validates a given JWT
    def is_authenticated(self):
        try:
            current_user = get_jwt_identity()
            jti = get_jwt()["jti"]  # JWT Token ID
            return self.check_token_validity(jti)
        except Exception as e:
            print(f"An error occurred: {e}")
            return {"AUTH": False, "Reason": "Unable to verify token"}

    # Checks if the token ID (jti) is valid and not revoked in the database
    def check_token_validity(self, jti):
        try:
            connection = SQLC.SQLConAdmin()
            connection.connect()
            result = connection.execute_query(SQLQ.SQLQueries.check_token_validity(jti))
            if result and result[0][0]:  # Assuming the query returns a boolean or similar to indicate validity
                return {"AUTH": True}
            else:
                return {"AUTH": False, "Reason": "Token invalid or revoked"}
        except Exception as e:
            print(f"An error occurred while checking token validity: {e}")
            return {"AUTH": False, "Reason": "Database error during token check"}
        finally:
            if connection:
                connection.close()

    # Logs out the user by marking the token ID as revoked
    def logout(self, user_id):
        try:
            jti = get_jwt()["jti"]  # JWT Token ID
            self.revoke_token(jti)
        except Exception as e:
            print(f"An error occurred while logging out: {e}")
            return False
        return True

    # Marks the token ID as revoked in the database
    def revoke_token(self, jti):
        try:
            connection = SQLC.SQLConAdmin()
            connection.connect()
            connection.execute_query(SQLQ.SQLQueries.revoke_token(jti))
            connection.cnx.commit()
        except Exception as e:
            print(f"An error occurred while revoking token: {e}")
            return False
        finally:
            if connection:
                connection.close()

    # Stores the token ID in the database for tracking purposes
    def store_token(self, user_id, jti):
        try:
            connection = SQLC.SQLConAdmin()
            connection.connect()
            connection.execute_query(SQLQ.SQLQueries.insert_token_id(jti, user_id))
            connection.cnx.commit()
        except Exception as e:
            print(f"An error occurred while storing token: {e}")
            return False
        finally:
            if connection:
                connection.close()
        return True

# Note: Remember to update SQL_AdminQuerys with the relevant queries for token handling
