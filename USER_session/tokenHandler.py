import uuid
import datetime
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt
from flask import request
from SQLAdminConnections import SQL_AdminConnector as SQLC
from SQLAdminConnections import SQL_AdminQuerys as SQLQ

class UserTokenHandler:
    def __init__(self):
        pass

    # Generates a JWT for a given user
    def login(self, user_id, expiry_minutes=60):
        additional_claims = {"user_id": user_id}
        expiry = datetime.timedelta(minutes=expiry_minutes)
        access_token = create_access_token(identity=user_id, additional_claims=additional_claims, expires_delta=expiry)
        jti = get_jwt()["jti"]  # Extracting the JTI from the token
        self.store_token(user_id, jti)  # Storing the token's JTI in the database
        return access_token

    # Validates a given JWT
    def is_authenticated(self):
        try:
            auth_header = request.headers.get('Authorization', None)
            if auth_header:
                token = auth_header.split()[1]  # Splitter 'Bearer <token>' og tar den andre delen
                return self.check_token_validity(token)
            else:
                return {"AUTH": False, "Reason": "No token provided"}
        except Exception as e:
            print(f"An error occurred: {e}")
            return {"AUTH": False, "Reason": "Unable to verify token"}

    # Checks if the token ID (jti) is valid and not revoked in the database
    def check_token_validity(self, token):
        try:
            connection = SQLC.SQLConAdmin()
            connection.connect()
            connection.execute_query(SQLQ.SQLQueries.use_users_database())
            result = connection.execute_query(SQLQ.SQLQueries.check_token_validity(token))
            if result and result[0][0]:  #query returns a boolean or similar to indicate validity
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
    def logout(self):
        try:
            user_identity = get_jwt_identity()  # Get the identity from the token
            user_id = user_identity["user_id"]  # Extracting the user ID
            self.revoke_tokens_by_user_id(user_id)
        except Exception as e:
            print(f"An error occurred while logging out: {e}")
            return False
        return True

    # Revokes all tokens for a given user
    def revoke_tokens_by_user_id(self, user_id):
        try:
            connection = SQLC.SQLConAdmin()
            connection.connect()
            connection.execute_query(SQLQ.SQLQueries.use_users_database())
            connection.execute_query(SQLQ.SQLQueries.revoke_tokens_by_user_id(user_id))
            connection.cnx.commit()
        except Exception as e:
            print(f"An error occurred while revoking tokens: {e}")
            return False
        finally:
            if connection:
                connection.close()
        return True

    # Stores the token ID in the database for tracking purposes
    def store_token(self, user_id, jti):
        try:
            connection = SQLC.SQLConAdmin()
            connection.connect()
            connection.execute_query(SQLQ.SQLQueries.use_users_database())
            connection.execute_query(SQLQ.SQLQueries.insert_token_id(jti, user_id))
            connection.cnx.commit()
        except Exception as e:
            print(f"An error occurred while storing token: {e}")
            return False
        finally:
            if connection:
                connection.close()
        return True
