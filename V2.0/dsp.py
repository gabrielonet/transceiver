#!/usr/bin/python
import time
import os
import sys
from time import sleep
from RPi import GPIO
sota_temp = 0
sota_center = 200
sota_bw = 200
timing = 0.0001
semaphor =0

GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.OUT) # Sota A
GPIO.setup(26, GPIO.OUT) # Sota B
GPIO.setup(21, GPIO.OUT) #Sota Reset 
GPIO.setup(9, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.OUT)  # Sota mode selection

GPIO.output(13, 0)
sleep(0.1)
GPIO.output(13, 1)
for x in reversed(range(100)):

            GPIO.output(19, 1)
            sleep(0.005)
            GPIO.output(26, 1)
            sleep(0.005)
            #GPIO.output(19, 1)
            #sleep(0.005)
            GPIO.output(19, 0)
            sleep(0.005)
            GPIO.output(26, 0)
            print 'wtf'
GPIO.output(13, 0)
sleep(0.1)
GPIO.output(13, 1)
for x in reversed(range(100)):
            GPIO.output(19, 1)
            sleep(0.005)
            GPIO.output(26, 1)
            sleep(0.005)
            #GPIO.output(19, 1)
            #sleep(0.005)
            GPIO.output(19, 0)
            sleep(0.005)
            GPIO.output(26, 0)
            

print 'pressing'
sleep(0.3)
GPIO.output(13, 0)
print 'pressing'
sleep(0.3)
GPIO.output(13, 1)


def sota_dsp(dsp_mode,start_x,stop_x):
    def sotabeam(greycode):
        global sota_bw
        global sota_center
        global sota_temp
        global sota_sleep
        global semaphor
        # detect if rotary right
        if dsp_mode.value == 0:   
            if (GPIO.input(10) == 0 and GPIO.input(9) == 1 and sota_temp == 0):

                   if 3500 > sota_bw >= 700:
                       sota_bw +=100
                   elif 700 > sota_bw >= 400:
                       sota_bw +=50
                   elif 400 > sota_bw >= 200 : 
                       sota_bw +=20               
                   sota_temp = 1

                   GPIO.output(26, 1)
                   sleep(timing)
                   GPIO.output(19, 1)
                   sleep(timing)
                   #GPIO.output(19, 1)
                   #sleep(sota_sleep)
                   GPIO.output(26, 0)
                   sleep(timing)
                   GPIO.output(19, 0)
                   sleep(timing)
                   
            # Rearm  left / right detection   
            if (GPIO.input(9) == 1 and GPIO.input(10) == 1):  
              sota_temp = 0 
            #detect rotary left   
            if (GPIO.input(10) == 1 and GPIO.input(9) == 0 and sota_temp == 0):     # if port 25 == 1  
                   if sota_bw >= 701:
                       sota_bw -=100
                   elif 700 >= sota_bw > 400:
                       sota_bw -=50
                   elif sota_bw > 200 : 
                       sota_bw -=20               
                   sota_temp = 1

                   GPIO.output(19, 1)
                   sleep(timing)
                   GPIO.output(26, 1)
                   sleep(timing)
                   GPIO.output(19, 1)
                   sleep(timing)
                   GPIO.output(19, 0)
                   sleep(timing)
                   GPIO.output(26, 0)
                   sleep(timing)
                   
        if dsp_mode.value == 1:   
            if (GPIO.input(10) == 0 and GPIO.input(9) == 1 and sota_temp == 0 and semaphor == 0):
                   semaphor = 1
                   if sota_center >= 2000:
                       sota_center +=50
                   elif 2000 > sota_center:
                       sota_center +=25
                   sota_temp = 1

                   GPIO.output(26, 1)
                   sleep(timing)
                   GPIO.output(19, 1)
                   sleep(timing)
                   GPIO.output(19, 1)
                   sleep(timing)
                   GPIO.output(26, 0)
                   sleep(timing)
                   GPIO.output(19, 0)
                   sleep(timing)
                   semaphor = 0
            # Rearm  left / right detection   
            if (GPIO.input(9) == 1 and GPIO.input(10) == 1 and semaphor == 0):  
              sota_temp = 0 
            #detect rotary left   
            if (GPIO.input(10) == 1 and GPIO.input(9) == 0 and sota_temp == 0 and semaphor == 0):     # if port 25 == 1  
                   semaphor = 1 
                   if sota_center >= 2000:
                       sota_center -=50
                   elif 2000 > sota_center > 200:
                       sota_center -=25
                  
                   sota_temp = 1

                   GPIO.output(19, 1)
                   sleep(timing)
                   GPIO.output(26, 1)
                   sleep(timing)
                   GPIO.output(19, 1)
                   sleep(timing)
                   GPIO.output(19, 0)
                   sleep(timing)
                   GPIO.output(26, 0)
                   sleep(timing)
                   semaphor = 0
            print sota_center       
                   

        start_x.value = (sota_center - int(sota_bw)/2) 
        stop_x.value =  (sota_center + int(sota_bw)/2)  
        if start_x.value < 200:
            start_x.value = 200
        if start_x.value > 3300:
            start_x.value = 3300
        if stop_x.value > 3500:
            stop_x.value = 3500



        
    start_x.value = (sota_center - int(sota_bw)/2) 
    stop_x.value =  (sota_center + int(sota_bw)/2) 
    GPIO.add_event_detect(10, GPIO.BOTH, callback=sotabeam)
    GPIO.add_event_detect(9 , GPIO.BOTH, callback=sotabeam) 

    
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print "good bye yo8rxp"
    





  


