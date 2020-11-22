from rejson import Client, Path
from timeloop import Timeloop
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.json_util import dumps

# start timeloop
tl = Timeloop()

# connect to queue
rj = Client(host='redis', port=6379, decode_responses=True)

#connect to database
client = MongoClient('mongo', 27017)
db = client.mydb

app = Flask(__name__) # initialize the flask app

rj.jsonset('tasks', Path.rootPath(), []) #initialize an empty array in the queue

@app.route('/add_task',methods=['POST'])
def send_to_queue():
    print("Sending task to queue...")
    data=request.get_json()
    rj.jsonarrinsert('tasks', Path.rootPath(), 0,data)
    return jsonify(data)

@app.route('/get_tasks')
def get_all_tasks():
    data=list(db['to-do'].find())
    return dumps(data)

@app.route('/update_task',methods=['POST'])
def update_task():
    task=request.get_json()['task']
    name=request.get_json()['name']
    myquery = {"task": task,"name":name}
    newvalues = {"$set": {'status': 'Done'}}
    db['to-do'].update_many(myquery,newvalues)
    return "successfully updated"


@app.route('/delete_task',methods=['POST'])
def delete_task():
    task=request.get_json()['task']
    name=request.get_json()['name']
    myquery = {"task": task,"name":name}
    db['to-do'].delete_many(myquery)
    return "successfully deleted"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
