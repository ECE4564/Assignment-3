# Assignment-3


### Storage Rpi
```
python3 storage.py
``` 

</br></br>

### LED Rpi
```
python3 led.py
```

> * Service Rpi: python3 service.py

> * Client system: Add user: bash add_user.sh <Service Server IP Address> 
Upload LED: bash upload-led.sh <Uploaded Filename> <Service Server IP>
Upload Storage: bash upload-storage.sh <Uploaded Filename> <Service Server IP>
  
</br>

### Libraries Used 

1. Flask - Framework for network applications that allows for the implementation of RESTful API’s.  This program used the request library inside of flask to handle the requests and gather relevant query variables.  Broadcasts the application on localhost at either a specified port or at port 5000 by default.

2. Zeroconf - The Zeroconf library initiates Zero-configuration networking inside of a Python script. It is used so that devices can be easily networked, without manually specifying addresses to each device for the other devices. 

3. RPi.GPIO - Library used to manipulate the GPIO pins of the Raspberry Pi.  The PWM function helped to change the duty cycle(on/off time) of the pulse to change the intensity of the LED.

4. Pymongo - Library for interacting with a MongoDB instance. In this case its functions were encapsulated in the MongoDB class. 

*In addition to the libraries listed above, Python built-in libraries such as logging, os, signal, json, and sys were used.*

<button class="button-save large">Big Fat Button</button>

### Contributions

David Toussaint: Fixed errors in MongoDB code from Assignment 2 in order to ensure StorageDB functioned correctly. The main issue was when buying or selling, if a count value was not provided an unhandled exception occurred. Created AuthDB class, which recycled code from the MongoDB class from Assignment 2, but reduced the number of functions to add() and find_user(). Controlled a NoSQL database via a RESTful API in the storage.py file. The database was the book database from Assignment 2, but flask was used to communicate with the storage Raspberry Pi over a RESTful interface. 

Michael Pocta: Laid the framework for all Flask implementations as well as fully implemented “led.py”, “LED_PWM.py” and “service.py”.  Implemented zeroconf functions to identify the IP address from the led and from the storage.  Correctly implemented the bash script sending, saving, and executing.  Implemented and debugged the connection between “service.py” and the rest of the system.
