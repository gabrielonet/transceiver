#!/usr/local/bin/python

import time
from time import sleep
from RPi import GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # VFO enc A
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP) # VFO enc B 
GPIO.setup(24, GPIO.OUT)

if __name__=='__main__':


    space = 0.3
    semafor = 0
    x=0

    
    def punct(bogus):
        print 'punct'
        GPIO.output(24, 1)
        sleep(space)
        GPIO.output(24, 0)
        speep(space)
         
    def linie(bogus):
        print 'linie'
        GPIO.output(24, 1)
        sleep(0.5)
        GPIO.output(24, 0)
        
    def apel(bogus):
        global space
        global semafor
        global x

        if (bogus == 18 and semafor == 0) :
            x+=1
            semafor = 1
            print 'linie'
            print x
            sleep(space)
            semafor = 0
            
            if GPIO.input(18) == 0:
              apel(18)






    print 'shit'
    GPIO.add_event_detect(18, GPIO.FALLING, callback=apel)
    #GPIO.add_event_detect(23, GPIO.FALLING, callback=apel)
 
    try:
        while True:
           sleep(1)
    except KeyboardInterrupt:
           print "good by yo8rxp"
           GPIO.cleanup()       # clean up GPIO on CTRL+C exit
    GPIO.cleanup()           # clean up GPIO on normal exit
