import StorageDB
from flask import Flask, request, jsonify
import subprocess
import os
import json

# Flask
app = Flask(__name__)


# ADD
@app.route('/book/add', methods=['POST'])
def add():
    content = request.json
    if content['Author'] is None:
        return 'Error: No data for Author'
    elif content['Name'] is None:
        return 'Error: No data for Name'
    else:
        db.insert(content)


# DELETE
@app.route('/book/delete', methods=['POST'])
def delete():
    content = request.json
    if content['Author'] is None:
        return 'Error: No data for Author'
    elif content['Name'] is None:
        return 'Error: No data for Name'
    else:
        db.remove(content)


# LIST
@app.route('/book/list', methods=['POST'])
def list_all():
    # TODO: Return message?
    return json.dumps(db.list_all(1))


# BUY
@app.route('/book/buy', methods=['POST'])
def buy():
    content = request.json
    if content['Author'] is None:
        return 'Error: No data for Author'
    elif content['Name'] is None:
        return 'Error: No data for Name'
    elif content['Count'] is None:
        return 'Error: No data for Count'
    else:
        db.change_stock(content['Author'], int(content['Count']))


# SELL
@app.route('/book/sell', methods=['POST'])
def sell():
    content = request.json
    if content['Author'] is None:
        return 'Error: No data for Author'
    elif content['Name'] is None:
        return 'Error: No data for Name'
    elif content['Count'] is None:
        return 'Error: No data for Count'
    else:
        change = int(content['Count'])
        db.change_stock(content['Author'], -change)


if __name__ == '__main__':
    db = StorageDB.MongoDB()
