#Imports libs
from flask import Flask, jsonify, request

#Init app
app = Flask(__name__)

#Get /test - data
@app.route('/get', methods=['GET'])
def testGet():
    #Returns set value
    return jsonify({"Dette er en": "get request"})

#POST /date - data
@app.route('/post', methods=['POST'])
def testPost():

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