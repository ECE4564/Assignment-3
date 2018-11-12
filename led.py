#!flask/bin/python
from flask import Flask, request, jsonify, json
import LED_PWM

import logging
import socket
import sys
import signal
from time import sleep

from zeroconf import ServiceInfo, Zeroconf 

app = Flask(__name__)

def signal_handler(sig, frame):
    print("Unregistering...")
    zeroconf.unregister_service(info)
    zeroconf.close()
    sys.exit(0)
    

@app.route('/LED/on', methods=['POST'])
def turnOn():
    led.turnOn()

    # Return message and code
    return "LED on"


@app.route('/LED/off', methods=['POST'])
def turnOff():
    led.turnOff()

    # Return message and code
    return "LED off"


@app.route('/LED', methods=['POST'])
def intensity():
    try:
        content = request.json
        color = content['color']
        intensity = content['intensity']
    except:
        return 'Invalid request, include intenisty data.'

    # Change the intensity of specified channel
    led.changeIntensity(color, intensity)

    # Return message and code
    return "Successfully set " + color + "'s intensity to " + str(intensity)


@app.route('/LED/info', methods=['GET'])
def info():
    led_vals = {}

    # Get all of the relevant information about LED
    led_vals["red"] = led.red_int
    led_vals["green"] = led.green_int
    led_vals["blue"] = led.blue_int
    led_vals["status"] = led.status

    return jsonify(led_vals)


if __name__ == '__main__':
    led = LED_PWM.LED_PWM()
    hostname = socket.gethostname()  
    IPAddr = socket.gethostbyname(hostname + ".local")
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) > 1:
        assert sys.argv[1:] == ['--debug']
        logging.getLogger('zeroconf').setLevel(logging.DEBUG)

    desc = {'path': '/~paulsm/'}

    info = ServiceInfo("_http._tcp.local.",
                       "LED._http._tcp.local.",
                       socket.inet_aton(str(IPAddr)), 5000, 0, 0,
                       desc, "ash-2.local.")

    zeroconf = Zeroconf()
    print("Registration of a service, press Ctrl-C to exit...")
    zeroconf.register_service(info)
    print("Ready for API calls")

    # Create clean exit signal
    signal.signal(signal.SIGINT, signal_handler)
        
    app.run(host= '0.0.0.0')
