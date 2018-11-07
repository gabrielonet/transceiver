#!/usr/bin/python
import time
import os
import sys
from time import sleep
from decimal import Decimal
import math
from math import floor
import fractions
from fractions import Fraction
from RPi import GPIO
from functools import partial

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # VFO enc A
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP) # VFO enc B 



lastA = GPIO.input(17)
lastB = GPIO.input(4)
x=0

def knob(greycode):
                global lastA
                global lastB
                global x
                last_grey = str(int(lastA))+str(int(lastB) )
                if greycode == 4:
                    lastA = not lastA
                    
                if greycode == 17:
                    lastB = not lastB    
                grey = str(int(lastA))+str(int(lastB) )
                if ( last_grey == "00" and grey == "01"):
                    x+=1
                if ( last_grey == "00" and grey == "10"):
                    x-=1                    
                print x



GPIO.add_event_detect(4, GPIO.BOTH, callback=partial(knob))
GPIO.add_event_detect(17, GPIO.BOTH, callback=partial(knob))

try:
        while True:
            sleep(0.1)
except KeyboardInterrupt:
        print "good bye yo8rxp"
        GPIO.cleanup()       # clean up GPIO on CTRL+C exit