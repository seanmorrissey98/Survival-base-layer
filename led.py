import serial
from nanpy import (ArduinoApi, SerialManager)
import time
import board
import neopixel
from time import sleep
import RPi.GPIO as GPIO

ledPin = 13

connection = SerialManager(device='/dev/ttyACM0')
a = ArduinoApi(connection = connection)
a.pinMode(ledPin, a.OUTPUT)

while True:
    a.digitalWrite(ledPin, a.HIGH)
    sleep(1)
    a.digitalWrite(ledPin, a.LOW)
    sleep(1)