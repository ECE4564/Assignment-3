#!flask/bin/python
from flask import Flask, request, jsonify, json
import subprocess
import os
import AuthDB
from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf
from time import sleep
import logging
import socket
from typing import cast

LED_IP = ""
STORE_IP = ""

class MyListener (object):
    def remove_service(self, zeroconf, type, name):
        print("Service%sremoved" % (name,))
    def add_service(self, zeroconf, type, name):
        # Global variables used for zeroconf
        global LED_IP
        global STORE_IP
        
        info = zeroconf.get_service_info(type, name)
        try:
            Name = info.name
        except:
            pass
        if(Name == "LED._http._tcp.local."):
            LED_IP = socket.inet_ntoa(cast(bytes, info.address))
        elif(Name == "STORAGE.http._tcp.local."):
            STORE_IP = socket.inet_ntoa(cast(bytes, info.address))

app = Flask(__name__)

# Upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'


@app.route('/add_user', methods=['POST'])
def add():
    try:
        userinfo = request.json
        username = userinfo['username']
        password = userinfo['password']
        res = auth_db.insert(userinfo)
        return res
    except:
        return 'Invalid request, missing information.'

    # Return message and code
    return "Successfully added " + username + " to the database."


@app.route('/upload/led', methods=['POST'])
def upload_LED():
    # Global variables used for zeroconf
    global LED_IP
    global STORE_IP
    
    try:
        auth = request.authorization
        #print('User: ' + auth.username + ' Password: ' + auth.password)
        found = auth_db.find_user(auth)
        if found:
            bashfile = request.files['file']
            filename = bashfile.filename
            # Saving file
            bashfile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            return 'User not found.'
    except:
        return 'Invalid request, no file included.'

    print("Running " + filename + " using IP: " + LED_IP + "..." )
    subprocess.Popen(["bash", os.path.join(app.config['UPLOAD_FOLDER'], filename), str(LED_IP)])

    # Return message and code
    return "LED file successfully uploaded."


@app.route('/upload/storage', methods=['POST'])
def upload_STORE():
    # Global variables used for zeroconf
    global LED_IP
    global STORE_IP
    
    try:
        auth = request.authorization
        #print('User: ' + auth.username + ' Password: ' + auth.password)
        found = auth_db.find_user(auth)
        if found:
            bashfile = request.files['file']
            filename = bashfile.filename
            # Saving file
            bashfile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            return 'User not found.'

    print("Running " + filename + " using IP: " + STORE_IP + "..." )
    subprocess.Popen(["bash", os.path.join(app.config['UPLOAD_FOLDER'], filename), str(STORE_IP)])

    # Return message and code
    return "Storage file successfully uploaded."


if __name__ == '__main__':
    auth_db = AuthDB.AuthDB()
    zeroconf = Zeroconf()
    listener = MyListener()
    browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)

    app.run(host= '0.0.0.0')
