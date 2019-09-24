import serial
from nanpy import (ArduinoApi, SerialManager)
import time
import board
import neopixel
from time import sleep
import RPi.GPIO as GPIO
import os
import time
import gpiozero
from gpiozero import Button

temp1Pin = 14
temp2Pin = 15
tempMult = .48828125

connection = SerialManager(device='/dev/ttyACM0')
a = ArduinoApi(connection = connection)
a.pinMode(temp1Pin, a.INPUT)

while True:
    value1 = a.analogRead(temp1Pin)
    value1 *= tempMult
    value2 = a.analogRead(temp2Pin)
    value2 *= tempMult
    avg_temp = (value1 + value2) / 2
    print("Temperature: " + str(avg_temp) +"*C")
    sleep(1)