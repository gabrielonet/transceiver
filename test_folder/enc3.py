# Define encoder count function
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

Encoder_A_old =    GPIO.input(4)  # store the current encoder values as old values to be used as comparison in the next loop
Encoder_B_old =   GPIO.input(17)
counts=0
error=0


def encodercount(term):
    global counts       
    global Encoder_A
    global Encoder_A_old
    global Encoder_B
    global Encoder_B_old
    global error
    Encoder_A = GPIO.input(17)  # stores the value of the encoders at time of interrupt
    Encoder_B = GPIO.input(4)

    if Encoder_A == Encoder_A_old and Encoder_B == Encoder_B_old:
    # this will be an error
        error += 1

    elif (Encoder_A == 1 and Encoder_B_old == 0) or (Encoder_A == 0 and Encoder_B_old == 1):
    # this will be clockwise rotation
        counts += 1
        print counts

    elif (Encoder_A == 1 and Encoder_B_old == 1) or (Encoder_A == 0 and Encoder_B_old == 0):
    # this will be counter-clockwise rotation
        counts -= 1
        print counts

    else:
    #this will be an error as well
        error += 1

    Encoder_A_old = Encoder_A     # store the current encoder values as old values to be used as comparison in the next loop
    Encoder_B_old = Encoder_B       
    # Initialize the interrupts - these trigger on the both the rising and falling 
GPIO.add_event_detect(17, GPIO.BOTH, callback = encodercount)   # Encoder A
GPIO.add_event_detect(4, GPIO.BOTH, callback = encodercount)   # Encoder B

# This is the part of the code which runs normally in the background
while True:
    time.sleep(1)