#!flask/bin/python
from flask import Flask, request, jsonify, json
import LED_PWM

app = Flask(__name__)

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
        color = content.color
        intensity = content.intensity
    except:
        return 'Invalid request, include intenisty data.'

    # Change the intensity of specified channel
    led.changeIntensity(color, intensity)

    # Return message and code
    return "Successfully set " + color + "'s intensity to " + str(intensity)

@app.route('/LED/off', methods=['GET'])
def turnOff():
    led.turnOff()
    # Return message and code
    return "LED off"


if __name__ == '__main__':
    led = LED_PWM()
    app.run(debug=True)
