#Imports libs
from flask import Flask, jsonify, request

#Init app
app = Flask(__name__)

#Get /test - data
@app.route('/test', methods=['GET'])
def hello():
    #Returns set value
    return jsonify({"Key": "Value"})

#POST /date - data
@app.route('/data', methods=['POST'])
def post_data():

    #Get data from POST request
    data = request.get_json()

    #print data
    print(data)

    #If POST request hhad no data,  return 400 error
    if not data:
        return jsonify({"Error": "No data"}), 400
    
    #Return data with 200 OK
    return jsonify(data)

# Run API
if __name__ == "__main__":
   app.run(debug=True, port=5001)