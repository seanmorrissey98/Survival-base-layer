import os
#to change audio output to 3.5mm jack run
#amixer cset numid=3 1
os.system("aplay /home/pi/Desktop/nanpy/alarm.wav")