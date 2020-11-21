from rejson import Client, Path
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
from flask_cors import CORS, cross_origin

#connect to database
client = MongoClient('localhost', 27017)
db = client.mydb

app = Flask(__name__) # initialize the flask app
cors = CORS(app) 
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/add_task',methods=['POST'])
def send_to_db():
    data=request.get_json()
    db['to-do'].insert_one(data)
    print("Sending json to database..")
    return data

@app.route('/get_tasks')
def get_all_tasks():
    data=list(db['to-do'].find())
    return dumps(data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
