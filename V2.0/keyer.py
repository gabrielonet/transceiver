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

def iambic(dummy,adc0):
    
    while True:
                tmp_speed = adc0.value
                speed = float((100-tmp_speed)/1000)
                if (GPIO.input(5)) == 0 :
                    GPIO.output(7, 1)  # set CW on
                    sleep(speed)    
                    GPIO.output(7, 0)  # set CW off
                    sleep(speed)    
                 
                if (GPIO.input(6)) == 0:
                    GPIO.output(7, 1)  # set CW on
                    sleep(speed*3)
                    GPIO.output(7, 0)  # set CW off
                    sleep(speed)    
    
    




  


