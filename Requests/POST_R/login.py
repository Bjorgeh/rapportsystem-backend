from http import HTTPStatus
from flask_restx import Resource
from flask import make_response, session, request, jsonify

# imports os
import os

current_directory = os.getcwd()
# imports sys
import sys

sys.path.append(os.path.join(current_directory))
from USER_session import sessionhandler as SH
from authorization import login_validation as login_auth
from Models import user_model as UM
from SQLAdminConnections import SQL_AdminConnector as SQLC
from SQLAdminConnections import SQL_AdminQuerys as SQLQ


# Login route
def login_route(ns):
    new_session = SH.UserSession(session)

    # Post request for login
    @ns.route("/login")
    class login(Resource):
        new_login_model = UM.login_model(ns)

        @ns.doc(
            "login",
            description="Logs user in when given Username and Password. This will create a new session for the user.",
            responses={
                200: "OK",
                400: "Invalid Argument or faulty data",
                401: "Incorrect credentials",
                500: "Internal server error",
            },
        )
        @ns.expect(new_login_model, validate=True)
        def post(self):
            # Checks if user is already logged in
            if "user_id" in session:
                new_session.update_session()
                return jsonify({"Error": "Already logged in"})

            data = request.get_json()
            username = data["username"].lower()
            password = data["password"]

            # Checks if username and password is ok
            login_validation = login_auth.loginValidation(
                username, password
            ).validate_credentials()

            # Variabler fra login_validation
            user_exists = login_validation[0]
            user_id = login_validation[1]
            user_accountType = login_validation[2]

            # Deletes old sessions for user
            delete_user_sessions(user_id)

            # creates new session for logged in user.
            if user_exists:
                # Lager ny session
                session["user_id"] = user_id
                session["email"] = username
                session["account_type"] = user_accountType
                # Her kan du sette inn flere detaljer i session om nødvendig

                print(username, "created new session")

                # Creates current user dict for returning data
                current_user = {
                    "user_id": session["user_id"],
                    "email": session["email"],
                    "accountType": session["account_type"],
                }

                # Returns success if username and password is ok
                if new_session.login():
                    return make_response(
                        {
                            "status": "Successful login",
                            "user_details": current_user,
                            "session_id": new_session.get_session_id(),
                        },
                        status=HTTPStatus.OK.value,  # 200
                    )

            # Returns error if username or password is wrong
            return make_response(
                {"error": "Invalid username or password"},
                HTTPStatus.UNAUTHORIZED.value,  # 401
            )


# fiction for removing old sessions
def delete_user_sessions(user_id):
    # connects to database
    connection = SQLC.SQLConAdmin()
    connection.connect()

    # query and params
    query, params = SQLQ.SQLQueries.delete_old_sessions_by_user_id(user_id)

    # Deletes old sessions
    try:
        result = connection.execute_query((query, params))
        connection.cnx.commit()

        # gets number of rows affected
        rows_affected = connection.cursor.rowcount
        if rows_affected == 0:
            print(f"No sessions found for user_id {user_id}.")
        else:
            print(f"Deleted {rows_affected} sessions for user_id {user_id}.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # closes connection
        connection.close()
