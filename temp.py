from nanpy import (ArduinoApi, SerialManager)
from time import sleep

ledPin = 7
buttonPin = 8
ledState = False
buttonState = 0

try:
    connection = SerialManager()
    a = ArduinoApi(connection = connection)
except:
    print("failed to connect to arduino")

a.pinMode(ledPin, a.OUTPUT)
a.pinMode(buttonPin, a.INPUT)

try:
    while True:
        buttonState = a.digitalRead(buttonPin)
        print("Our button state is: {}".format(buttonState))
        if buttonState:
            if ledState:
                a.digitalWrite(ledPin, a.LOW)
                ledState = False
                print("LED OFF")
                sleep(1)
            else:
                a.digitalWrite(ledPin, a.HIGH)
                ledState = True
                print("LED ON")
except:
    a.digitalWrite(ledPin, a.LOW)
