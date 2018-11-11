import RPi.GPIO as GPIO
import time

red = 16
green = 20
blue = 21

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setup(red,GPIO.OUT)
GPIO.setup(green,GPIO.OUT)
GPIO.setup(blue,GPIO.OUT)

 # 50Hz PWM Frequency  
pwm_red = GPIO.PWM(red, 50)
pwm_green = GPIO.PWM(green, 50)
pwm_blue = GPIO.PWM(blue, 50)

 # Full Brightness, 100% Duty Cycle  
 

class LED_PWM:
    def __init__(self):
        self.red_int = 100
        self.green_int = 100
        self.blue_int = 100
        self.status = 0

    def turnOn(self):
        # Turn on LED with saved intensity values
        pwm_red.start(self.red_int)
        pwm_green.start(self.green_int)
        pwm_blue.start(self.blue_int)
        self.status = 1

    def turnOff(self):
        # Turn off every LED
        pwm_red.start(0)
        pwm_green.start(0)
        pwm_blue.start(0)
        self.status = 0

    def changeIntensity(self, color, intensity):
        # Determine which color to change
        if color == 'red':
            self.red_int = intensity
            pwm_red.start(self.red_int)
        elif color == 'green':
            self.green_int = intensity
            pwm_green.start(self.green_int)
        elif color == 'blue':
            self.blue_int = intensity
            pwm_blue.start(self.blue_int)
