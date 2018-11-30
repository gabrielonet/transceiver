#!/usr/bin/python
from __future__ import division

import time
import os
import sys

from time import sleep
import Adafruit_ADS1x15



from RPi import GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(7, GPIO.OUT)
GPIO.output(7, 0)  # set key off


GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Dah
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Dit 

def iambic():
    adc = Adafruit_ADS1x15.ADS1115()
    while True:
                speed = float(adc.read_adc(0, 1)/10000)
                if (GPIO.input(5)) == 0 :
                    GPIO.output(7, 1)  # set CW on
                    print 'dah'
                    sleep(speed)    
                    GPIO.output(7, 0)  # set CW off
                    sleep(speed)    
                 
                if (GPIO.input(6)) == 0:
                    GPIO.output(7, 1)  # set CW on
                    print 'dit '
                    sleep(speed*3)
                    GPIO.output(7, 0)  # set CW off
                    sleep(speed)    

    
    




  


