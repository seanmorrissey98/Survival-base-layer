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


import os
from gps3.agps3threaded import  AGPS3mechanism
from time import *
import time
import threading 
 
os.system('clear')



counter = 0
innerCounter = 0
counterWarn3 = 0
previous_counter = 0
pixel_pin = board.D12
num_pixels = 138
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False,
                           pixel_order=ORDER)
GPIO.setmode(GPIO.BCM)
temp1Pin = 14
temp2Pin = 15
flexPin = 16
ledPin = 18
tempMult = .48828125
pulse = 0
button = Button(10)
connection = SerialManager(device='/dev/ttyACM0')
a = ArduinoApi(connection = connection)
a.pinMode(temp1Pin, a.INPUT)
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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
        
agps_thread=AGPS3mechanism()
agps_thread.stream_data()
agps_thread.run_thread()
    
while True:
    while True:
        #pixels.fill((0,0,0))
        #pixels.show()
        #button pressed and released
        #if button.is_pressed:
            #button.wait_for_release()
            #counter += 1
            #counter += 1
       
        button_state = GPIO.input(23)
        if button_state == False:
            counter += 1
            #print("button pressed")
    
        #switch case using counter
        if counter == previous_counter:
            break
        else:
            #1
            #speaker "temperature low"
            if counter == 1:
                os.system("omxplayer -o hdmi ~/Desktop/nanpy/warning1.wav")
                os.system('clear')
                print("warning 1 played\n")
            #2
            #led mock heating pads
            elif counter == 2:
                rainbow_cycle(0.001)
                pixels.show()
                
            #3
            #another speaker warning about dangerous temperature
            elif counter == 3:
                if counterWarn3 == 0:
                    pixels.fill((0,0,0))
                    pixels.show()
                    os.system("omxplayer -o hdmi ~/Desktop/nanpy/warning2.wav")
                    os.system('clear')
                    print("warning 2 played\n")
                
                rainbow_cycle(0.001)
                pixels.show()
                    
               #
            #4
            #speaker announcing "transmitting gps signal
            #led blinking on shoulder
            #gps data output to screen
            #temperature and pulse output too
            elif counter == 4:
                if (innerCounter % 4) == 0:
                    pixels.fill((0,0,0))
                    pixels.show()
                    os.system("omxplayer -o hdmi ~/Desktop/nanpy/warning3.wav")
                    os.system('clear')
                    print("warning 3 played\n")
                
                rainbow_cycle(0.001)
                pixels.show()
                a.pinMode(ledPin, a.OUTPUT)  
                for blink in range(3):
                    a.digitalWrite(ledPin, a.HIGH)
                    sleep(.5)
                    a.digitalWrite(ledPin, a.LOW)
                    sleep(.5)
                a.pinMode(temp1Pin, a.INPUT)
                value1 = a.analogRead(temp1Pin)
                value1 *= tempMult
                value2 = a.analogRead(temp2Pin)
                value2 *= tempMult
                avg_temp = (value1 + value2) / 2
                
                #print gps code out
                print("GPS: ")
                print("    Latitude: ", agps_thread.data_stream.lat)
                print("    Longitude: ",agps_thread.data_stream.lon)
                # Temperature code
                print("Temperature: " + str(avg_temp) +"*C")
                
                #pulse code
                if (innerCounter % 3) == 0:
                    print("Pulse: 40\n")
                elif (innerCounter % 2) == 0:
                    print("Pulse: 42\n")
                else:
                    print("Pulse: 41\n")
                    
                innerCounter+=1
                break
                
            elif counter == 5:
                counter = 0
                pixels.fill((0,0,0))
                pixels.show()
        
        sleep(3)
        #button_state = True
        previous_counter = counter