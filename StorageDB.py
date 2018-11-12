from flask import Flask, request, jsonify
import json
import MongoDB
import logging
import socket
import sys
import signal

from zeroconf import ServiceInfo, Zeroconf

# Flask
app = Flask(__name__)


def signal_handler(sig, frame):
    print("Unregistering...")
    zeroconf.unregister_service(info)
    zeroconf.close()
    sys.exit(0)


# ADD
@app.route('/book/add', methods=['POST'])
def add():
    content = request.json
    if content['Author'] is None:
        return 'Error: No data for Author'
    elif content['Name'] is None:
        return 'Error: No data for Name'
    else:
        res = db.insert(content)
        return res


# DELETE
@app.route('/book/delete', methods=['DELETE'])
def delete():
    content = request.json
    if content['Author'] is None:
        return 'Error: No data for Author'
    elif content['Name'] is None:
        return 'Error: No data for Name'
    else:
        res = db.remove(content)
        return res


# LIST
@app.route('/book/list', methods=['GET'])
def list_all():
    # TODO: Return message?
    return json.dumps(db.list_all(1))


# BUY
@app.route('/book/buy', methods=['PUT'])
def buy():
    content = request.json
    if content['Author'] is None:
        return 'Error: No data for Author'
    elif content['Name'] is None:
        return 'Error: No data for Name'
    elif content['Count'] is None:
        return 'Error: No data for Count'
    else:
        res = db.change_stock(content['Author'], int(content['Count']))
        return res


# SELL
@app.route('/book/sell', methods=['PUT'])
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
        res = db.change_stock(content['Author'], -change)
        return res


@app.route('/book/count?Action=COUNT&<Name>&<Author>', methods=['GET'])
def count(Name, Author):
    res = db.get_count(Name)
    return res


if __name__ == '__main__':
    db = MongoDB.MongoDB()
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname + ".local")
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) > 1:
        assert sys.argv[1:] == ['--debug']
        logging.getLogger('zeroconf').setLevel(logging.DEBUG)

    desc = {'path': '/~paulsm/'}

    info = ServiceInfo("_http._tcp.local.",
                       "STORAGE._http._tcp.local.",
                       socket.inet_aton(str(IPAddr)), 5000, 0, 0,
                       desc, "ash-2.local.")

    zeroconf = Zeroconf()
    print("Registration of a service, press Ctrl-C to exit...")
    zeroconf.register_service(info)
    print("Ready for API calls")

    # Create clean exit signal
    signal.signal(signal.SIGINT, signal_handler)

    app.run(host='0.0.0.0')
