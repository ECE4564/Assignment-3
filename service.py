#!flask/bin/python
from flask import Flask, request, jsonify, json
import subprocess
import os
#import AuthDB
from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf
from time import sleep
import logging
import socket
from typing import cast

LED_IP = ""

class MyListener (object):
    def remove_service(self, zeroconf, type, name):
        print("Service%sremoved" % (name,))
    def add_service(self, zeroconf, type, name):
        global LED_IP
        info = zeroconf.get_service_info(type, name)
        try:
            Name = info.name
        except:
            pass
        print(Name)
        if(Name == "LED._http._tcp.local."):
            LED_IP = socket.inet_ntoa(cast(bytes, info.address))
            print(LED_IP + '\n')
            zeroconf.close()

app = Flask(__name__)

# Upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'


@app.route('/add_user', methods=['POST'])
def add():

    # Return message and code
    return "LED on"


@app.route('/upload/led', methods=['POST'])
def upload_LED():
    global LED_IP
    try:
        bashfile = request.files['file']
        filename = bashfile.filename
    except:
        return 'Invalid request, no file included.'

    # Saving file
    bashfile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    print("Running " + filename + "...")
    # Need to change IP to zeroconf obtained IP
    print(str(LED_IP) + '\n')
    subprocess.Popen(["bash", os.path.join(app.config['UPLOAD_FOLDER'], filename), str(LED_IP)])

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
    zeroconf = Zeroconf()
    listener = MyListener()
    browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)

    app.run(host= '0.0.0.0', port=5002)
    
#     try:
#         while True:
#             sleep(0.1)
#     except KeyboardInterrupt:
#         pass
#     finally:
#         zeroconf.close()

