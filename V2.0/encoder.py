#!/usr/bin/python
import time
import os
import sys
from time import sleep
from decimal import Decimal
from Si5351 import Si5351 
import math
from math import floor
import fractions
from fractions import Fraction
from RPi import GPIO
import Adafruit_MCP4725
dac = Adafruit_MCP4725.MCP4725(address=0x61, busnum=1)



GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # VFO enc A
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP) # VFO enc B 
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # RIT enc A
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP) # RIT enc B 
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP) # PTT 
GPIO.setup(12, GPIO.OUT)  # Tx/Rx Relay 
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # arduino PTT 

GPIO.output(12, 0)  # set TX/RX ro RX

GPIO.setup(14, GPIO.OUT)  # A - Band Relay
GPIO.setup(15, GPIO.OUT)  # B  -Band Relay
GPIO.setup(18, GPIO.OUT)  # C  -Band Relay
GPIO.setup(16, GPIO.OUT)  #  Key out
GPIO.setup(16, 0)  #  Key out to transmit

encoder_temp = 0
rit_temp = 0
rit_rx_enc = 0
rit_tx_enc = 0
semaphor = 0

def buttons(freq,step,tcvr_status,rit,rit_rx,rit_tx,touch_event,af_pre,bfo, full_break):
    def knob(greycode):
                global encoder_temp
                # detect if rotary right
                if (GPIO.input(17) == 0 and GPIO.input(4) == 1 and encoder_temp == 0):   
                    encoder_temp = 1
                    freq.value+=step.value
                    vfo()
                # Rearm  left / right detection   
                if (GPIO.input(4) == 1 and GPIO.input(17) == 1):  
                    encoder_temp = 0               
                #detect rotary left   
                if (GPIO.input(17) == 1 and GPIO.input(4) == 0 and encoder_temp == 0):     
                    encoder_temp = 1                                    
                    freq.value-=step.value
                    vfo()
        
            
    def clarifier(greycode):
            global rit_temp
            global rit_rx_enc
            global rit_tx_enc
            global semaphor
            if (rit_rx.value == 1 and tcvr_status.value == 0): 
                # detect if rotary right
                if (GPIO.input(22) == 0 and GPIO.input(27) == 1 and rit_temp == 0 and semaphor == 0):
                    semaphor = 1
                    rit_temp = 1
                    rit_rx_enc+=0.00001
                    rit.value = rit_rx_enc
                    semaphor = 0
                # Rearm  left / right detection   
                if (GPIO.input(22) == 1 and GPIO.input(27) == 1 and semaphor == 0):
                    rit_temp = 0               
                #detect rotary left   
                if (GPIO.input(22) == 1 and GPIO.input(27) == 0 and rit_temp == 0 and semaphor == 0):
                    semaphor  = 1
                    rit_temp =1
                    rit_rx_enc-=0.00001
                    rit.value = rit_rx_enc
                    semaphor = 0
                vfo()
                #integrat(freq.value+rit_rx_enc)

            if  (rit_tx.value == 1 and tcvr_status.value == 1 and semaphor == 0)  :    
                # detect if rotary right
                if (GPIO.input(22) == 0 and GPIO.input(27) == 1 and rit_temp == 0):
                    semaphor = 1
                    rit_temp = 1
                    rit_tx_enc+=0.01
                    rit.value = rit_tx_enc
                    semaphor = 0
                # Rearm  left / right detection   
                if (GPIO.input(22) == 1 and GPIO.input(27) == 1 and semaphor == 0):  
                    rit_temp = 0               
                #detect rotary left   
                if (GPIO.input(22) == 1 and GPIO.input(27) == 0 and rit_temp == 0):
                    semaphor = 1
                    rit_temp=1
                    rit_tx_enc-=0.01
                    rit.value = rit_tx_enc
                    semaphor = 0
                integrat(freq.value+rit_tx_enc/100)


    def vfo_level(*args):
                if 0 <= freq.value <=5:
                    if tcvr_status.value == 0 :
                         dac.set_voltage(1200)
                    else: 
                        dac.set_voltage(1130)
                if 5 < freq.value <=9:
                    if tcvr_status.value == 0 :
                         dac.set_voltage(1265)
                    else: 
                        dac.set_voltage(0)
                if 9 < freq.value <=18:
                    if tcvr_status.value == 0 :
                         dac.set_voltage(1265)
                    else: 
                        dac.set_voltage(0)
                if 18 < freq.value <=24:
                    if tcvr_status.value == 0 :
                         dac.set_voltage(1265)
                    else: 
                        dac.set_voltage(0)                        
                if 24 < freq.value <=30:
                    if tcvr_status.value == 0 :
                         dac.set_voltage(1265)
                    else: 
                        dac.set_voltage(0)
                        
           
                        
                        
                        
                        
                        

    def ptt(*args):
            global rit_rx_enc
            global rit_tx_enc
            if  ( GPIO.input(11) == 0 or (GPIO.input(5) == 0 and full_break.value == 1) ):
                GPIO.output(20, 1)
                GPIO.output(12, 1) 
                tcvr_status.value = 1
            else:
                GPIO.output(12, 0)             
                tcvr_status.value = 0
                rit.value = rit_rx_enc
                if af_pre.value == 1:
                    GPIO.output(20, 0)
            
            vfo()
            

    def vfo():
            global rit_rx_enc
            global rit_tx_enc
            if tcvr_status.value == 0:
                si_freq =  freq.value + rit_rx_enc + 9.0005 + bfo.value
            else:
                si_freq = freq.value + rit_tx_enc
            integrat(si_freq)
            #print bfo.value
    #def bfo():
            ## Set bfo for USB/LSB filter (9 mhz sharp)
            ##si.setupPLL(si.PLL_B, 21, 6, 10)
            ##si.setupMultisynth(1, si.PLL_B, 60)
            ## Set bfo for USB/LSB filter (9 mhz sharp)
            #si.setupPLL(si.PLL_B, 28, 1039, 12500)
            #si.setupMultisynth(1, si.PLL_B, 78)
            vfo_level()

    rit.value = 0
    tcvr_status.value = 0
    si = Si5351()
    si.enableOutputs(True)  

    def integrat(freq):
        vco=970
        div=int(vco/freq)
        vco=freq*div
        ratio=vco/25
        a=int(floor(ratio))
        fra_ction=ratio-a
        bc_division=(Fraction(fra_ction).limit_denominator(1048575))
        if (bc_division == 0):
            b=0
            c=1
        b=int(str(bc_division).split("/")[0])
        if (b > 0):
            c=int(str(bc_division).split("/")[1])  
        si.setupPLL(si.PLL_A, a, b, c)
        si.setupMultisynth(2, si.PLL_A, div)

    
    def touch_rit():
        print 'touch screen RIT event happened'
        vfo()
        vfo_level()

    
    GPIO.add_event_detect(4, GPIO.BOTH, callback=knob)
    GPIO.add_event_detect(17, GPIO.BOTH, callback=knob)
    GPIO.add_event_detect(22, GPIO.BOTH, callback=clarifier)
    GPIO.add_event_detect(27, GPIO.BOTH, callback=clarifier)
    GPIO.add_event_detect(11, GPIO.BOTH, callback=ptt)
    GPIO.add_event_detect(5, GPIO.BOTH, callback=ptt)
    vfo() #  generate VFO freq at reboot
    #bfo() #  generate BFO freq at reboot 
    try:
        while True:
            ## this is the place where main process c_types value changes are executing shit inside loop on sleep timing  bases without using observer as variable changes event
            sleep(0.1)
            if  touch_event.value !=  0:
                if touch_event.value == 1:
                    touch_rit()

                if str(touch_event.value).startswith(('2')) == True:
                    if touch_event.value == 235:
                        print 'relay 80 meters'
                        #GPIO.output(14, 0)  
                        #GPIO.output(15, 0) 
                        #GPIO.output(18, 0)  
                        freq.value = 3.5
                        vfo()
                    if touch_event.value == 27:
                        print 'relay 40 meters'
                        #GPIO.output(14, 1)  
                        #GPIO.output(15, 0) 
                        #GPIO.output(18, 0)  
                        freq.value = 7
                        vfo()
                    if touch_event.value == 214:
                        print 'relay 20 meters'
                        #GPIO.output(14, 0)  
                        #GPIO.output(15, 1) 
                        #GPIO.output(18, 0)
                        freq.value = 14
                        vfo()
                    if touch_event.value == 221:
                        print 'relay 15 meters'
                        #GPIO.output(14, 1)  
                        #GPIO.output(15, 1) 
                        #GPIO.output(18, 0)
                        freq.value = 21
                        vfo()
                        
                    if touch_event.value == 228:
                        print 'relay 10 meters'
                        #GPIO.output(14, 0)  
                        #GPIO.output(15, 0) 
                        #GPIO.output(18, 1) 
                        freq.value = 28
                        vfo()
                if str(touch_event.value).startswith(('3')) == True:
                    if touch_event.value == 323:
                        bfo.value =0
                        vfo()
                    if touch_event.value == 325:
                        bfo.value = 0
                        vfo()
                    if touch_event.value == 38:
                        bfo.value = 0.001
                        vfo()                        


                touch_event.value = 0
    except KeyboardInterrupt:
        print "good bye yo8rxp"
        GPIO.cleanup()       # clean up GPIO on CTRL+C exit
    




  


