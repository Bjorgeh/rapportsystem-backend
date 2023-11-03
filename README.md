<h1>rapportsystem-backend<h/>

Before clone:<br>

Install pip:<br>
python3 get-pip.py<br>

mySqlConnector:<br>
pip install mysql-connector-python<br>

Flask:<br>
pip install Flask<br>
pip install flask-restx<br>
pip install flask-session<br>

Bcrypt:
pip install bcrypt<br>

Secret file:<br>
Make ./SQLConnector/secret.py, with content:<br>
host_IP = 'YOUR MYSQL SERVER IP'<br>
host_user = 'YOUR USERNAME'<br>
host_password = 'YOUR PASSWORD'<br>
host_database = 'TARGET DATABASE'<br>
simple_query = 'YOUR SQL QUERY' <br>

or, if collab: download secret.py from teams chat.
