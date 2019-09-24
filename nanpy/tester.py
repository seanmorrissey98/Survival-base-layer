import serial
from nanpy import (ArduinoApi, SerialManager)
import time
import board
import neopixel
from time import sleep
import RPi.GPIO as GPIO


import os
from gps3.agps3threaded import  AGPS3mechanism
from time import *
import time
import threading 
 
os.system('clear') #clear the terminal (optional)
 

temp1Pin = 14
temp2Pin = 15
flexPin = 16
ledPin = 13
tempMult = .48828125
VCC = 4.98
R_DIV = 47500.0
STRAIGHT_RESISTANCE = 37300.0
BEND_RESISTANCE = 90000.0
VARIANCE = 10
MAX_TIME = 150
prevFlexR = 0
flexR = 0
moveTime = 0
pulse = 0
pixel_pin = board.D12
num_pixels = 138
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False,
                           pixel_order=ORDER)
GPIO.setmode(GPIO.BCM)
red_pin = 18
GPIO.setup(red_pin, GPIO.OUT)
low_temp = 35
dangerous_temp = 32
base_pulse = 60
no_move_time = 3


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)
        
def fade_red():
    while True:
        for j in range(255):
            for i in range(num_pixels):
                pixels.fill((j,0,0))
                pixels.show()
        for k in range(255):
            for m in range(num_pixels):
                pixels.fill((255-(k),0,0))
                pixels.show()

connection = SerialManager(device='/dev/ttyACM0')
a = ArduinoApi(connection = connection)
a.pinMode(temp1Pin, a.INPUT)


try:
    #GPS thread 
    agps_thread=AGPS3mechanism()
    agps_thread.stream_data()
    agps_thread.run_thread()
    
    while True:
        value1 = a.analogRead(temp1Pin)
        value1 *= tempMult
        value2 = a.analogRead(temp2Pin)
        value2 *= tempMult
        avg_temp = (value1 + value2) / 2
        #avg_temp -= 30
        #GPS-Sample --->Remove  it out  later
        print("Sample Latitude try ", agps_thread.data_stream.lat)
        print(" and  long ",agps_thread.data_stream.lon)
        print("Temperature: " + str(avg_temp) +"*C")
        flexADC = a.analogRead(flexPin)
        flexV = flexADC * VCC / 1023.0
        prevFlexR = flexR
        flexR = R_DIV * (VCC / flexV - 1.0)
        print("flex:")
        print(flexR)
        #time.sleep(1)
        
        if abs(flexR - prevFlexR) < 1000:
            moveTime += 1
            #print("Movetime : " + str(moveTime)+"\n")
            
        else:
            moveTime = 0
            
        if avg_temp < low_temp:
            rainbow_cycle(0.001)
            print("Speaker Warning: Temperature low\n")#swap in speaker transmission here when arrives
            #to change audio output to 3.5mm jack run
            #amixer cset numid=3 1
            os.system("aplay /home/pi/Desktop/nanpy/alarm.wav")
            pixels.show()
            #import light
            
            if avg_temp < dangerous_temp:
                print("Speaker Warning: temperature dangerously low\n")
                #to change audio output to 3.5mm jack run
                #amixer cset numid=3 1
                os.system("aplay /home/pi/Desktop/nanpy/alarm.wav")
                if moveTime > no_move_time and pulse < base_pulse:
                    #to change audio output to 3.5mm jack run
                    #amixer cset numid=3 1
                    os.system("aplay /home/pi/Desktop/nanpy/alarm.wav")
                    print("Speaker Warning: Sending GPS coordinates ("+ agps_thread.data_stream.lat+" , "+ agps_thread.data_stream.lon+") and vitals to personnel\n")
                    #GPIO.output(red_pin, True) #activate led on shoulder
                    a.pinMode(ledPin, a.OUTPUT)
                    
                    for blink in range(3):
                        a.digitalWrite(ledPin, a.HIGH)
                        sleep(.5)
                        a.digitalWrite(ledPin, a.LOW)
                        sleep(.5)
                        
                    time.sleep(0.5)
                    a.pinMode(temp1Pin, a.INPUT)
                    #import gpsdData  #output to screen GPS
                    
        else:
            pixels.fill((255,0,0))
            pixels.show()
        #sleep(1)
            
except:
    GPIO.cleanup()
    print(traceback.format_exc())

    print("\nTurning off.")
