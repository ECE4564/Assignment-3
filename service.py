#!flask/bin/python
from flask import Flask, request, jsonify, json
import subprocess
import os
#import AuthDB

app = Flask(__name__)

# Upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'


@app.route('/add_user', methods=['POST'])
def add():

    # Return message and code
    return "LED on"


@app.route('/upload/led', methods=['POST'])
def upload_LED():
    try:
        bashfile = request.files['file']
        filename = bashfile.filename
    except:
        return 'Invalid request, no file included.'

    # Saving file
    bashfile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    print("Running " + filename + "...")
    # Need to change IP to zeroconf obtained IP
    subprocess.Popen(["bash", os.path.join(app.config['UPLOAD_FOLDER'], filename), "192.168.1.36"])

    # Return message and code
    return "File successfully uploaded."


@app.route('/upload/storage', methods=['POST'])
def upload_STORE():
    try:
        bashfile = request.files['file']
        filename = bashfile.filename
    except:
        return 'Invalid request, no file included.'

    # Saving file
    bashfile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    print("Running " + filename + "...")
    # Need to change IP to zeroconf obtained IP
    subprocess.Popen(["bash", os.path.join(app.config['UPLOAD_FOLDER'], filename), "192.168.1.36"])

    # Return message and code
    return "File successfully uploaded."


if __name__ == '__main__':
    #auth = AuthDB()
    app.run(host= '0.0.0.0', port=5002)
