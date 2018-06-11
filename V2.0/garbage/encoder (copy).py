#!/usr/bin/python
import time
import os
import sys
from time import sleep
from RPi import GPIO
from decimal import Decimal
from Si5351 import Si5351 
import math
from math import floor
import fractions
from fractions import Fraction



#Clock Builder



def integrat(freq):
    for vco in range(610,890):
     div=int(vco/freq)
     if (900 < div > 8 ): 
      break
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
    #print "compute freq = "+str(freq)
    si.setupPLL(si.PLL_A, a, b, c)
    si.setupMultisynth(0, si.PLL_A, div)
    si.enableOutputs(True)	    





## define rotary encoder init setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)



if __name__=='__main__':
        
    freq =  open('/dev/shm/freq').read().rstrip()
    freq = float(freq)
    step = 0.00001
    si = Si5351() 
    si.enableOutputs(True)
    integrat(freq)
    encoder_temp = 1
    def rotary(greycode):
           step = float(open('/dev/shm/step').read().rstrip())
           global encoder_temp
           global freq
           # detect if rotary right
           if (GPIO.input(17) == 0 and GPIO.input(18) == 1 and encoder_temp == 0):     # if port 25 == 1  
	      if freq <259.00001 :
                 freq +=step
                 fifo = open('/dev/shm/freq','w')
                 fifo.write(repr(freq))
                 fifo.close()
                 integrat(freq)
              encoder_temp = 1
           # Rearm  left / right detection   
           if (GPIO.input(17) == 1 and GPIO.input(18) == 1):  
              encoder_temp = 0 
           #detect rotary left   
           if (GPIO.input(17) == 1 and GPIO.input(18) == 0 and encoder_temp == 0):     # if port 25 == 1  
              if freq > 0.10000 : 
                 freq -=step
                 fifo = open('/dev/shm/freq','w')
                 fifo.write(repr(freq))
                 fifo.close()
                 integrat(freq)
              encoder_temp = 1 
    def xmit(*args):
       global freq
       mode_offset = 0.001
       if  GPIO.input(4) == 0 :
	   integrat(freq)
       else:
           integrat(freq+mode_offset)

    rit_r_temp = 1
    rit_t_temp = 1
    rit_rx = 0
    rit_tx = 0
    def clarifier(greycode):
           tcvr_state = open('/dev/shm/tcvr_status').read().rstrip()
           if tcvr_state == 'rx':
               mode = 'rx'
           else: mode = 'tx'    


           inhibit_rx_rit = open('/dev/shm/rit_rx_status').read().rstrip()
	   if inhibit_rx_rit == 'on' :
	    if mode == 'rx' : 

		  rit_r = open('/dev/shm/rit_rx').read().rstrip()
		  if rit_r == '0.00':
		      rit_rx = 0  
		  global rit_r_temp
		  global rit_rx
		  # detect if rotary right
		  if (GPIO.input(22) == 0 and GPIO.input(27) == 1 and rit_r_temp == 1):   
		      rit_rx +=0.01
		      rit_rx_1 =  "%0.2f" % Decimal(rit_rx)
		      rit_r_temp = 0
		      rit_r = open('/dev/shm/rit_rx','w')
		      rit_r.write(rit_rx_1)
		      rit_r.close()                 
		    
		  # Rearm  left / right detection   
		  if (GPIO.input(22) == 1 and GPIO.input(27) == 1):  
			rit_r_temp = 1               
		  #detect rotary left   

		  if (GPIO.input(22) == 1 and GPIO.input(27) == 0 and rit_r_temp == 1):     # if port 25 == 1  
			rit_rx -=0.01
			rit_r_temp = 0
			rit_rx_1 =  "%0.2f" % Decimal(rit_rx)
			rit_r = open('/dev/shm/rit_rx','w')
			rit_r.write(rit_rx_1)
			rit_r.close()
		  
           inhibit_tx_rit = open('/dev/shm/rit_tx_status').read().rstrip()
	   if inhibit_tx_rit == 'on' :	  
	    if mode == 'tx' : 
		  rit_t = open('/dev/shm/rit_tx').read().rstrip()
		  if rit_t == '0.00':
		      rit_tx = 0  
		  global rit_t_temp
		  global rit_tx
		  # detect if rotary right
		  if (GPIO.input(22) == 0 and GPIO.input(27) == 1 and rit_t_temp == 1):   
		      rit_tx +=0.01
		      rit_tx_1 =  "%0.2f" % Decimal(rit_tx)
		      rit_t_temp = 0
		      rit_t = open('/dev/shm/rit_tx','w')
		      rit_t.write(rit_tx_1)
		      rit_t.close()                 
		    
		  # Rearm  left / right detection   
		  if (GPIO.input(22) == 1 and GPIO.input(27) == 1):  
			rit_t_temp = 1               
		  #detect rotary left   

		  if (GPIO.input(22) == 1 and GPIO.input(27) == 0 and rit_t_temp == 1):     # if port 25 == 1  
			rit_tx -=0.01
			rit_t_temp = 0
			rit_tx_1 =  "%0.2f" % Decimal(rit_tx)
			rit_t = open('/dev/shm/rit_tx','w')
			rit_t.write(rit_tx_1)
			rit_t.close()  
			



    tcvr_state = 'rx' 
    def xmit(*args):
       global freq
       mode_offset = 0.001
       if  GPIO.input(4) == 0 :
	   integrat(freq)
	   tcvr_state = 'rx'
       else:
           integrat(freq+mode_offset) 
           tcvr_state = 'tx'
 
    
    GPIO.add_event_detect(17, GPIO.BOTH, callback=rotary)
    GPIO.add_event_detect(18, GPIO.BOTH, callback=rotary)
    GPIO.add_event_detect(22, GPIO.BOTH, callback=clarifier)
    GPIO.add_event_detect(27, GPIO.BOTH, callback=clarifier)
    try:
        while True:
           sleep(1)
    except KeyboardInterrupt:
           print "good by yo8rxp"
           GPIO.cleanup()       # clean up GPIO on CTRL+C exit
    GPIO.cleanup()           # clean up GPIO on normal exit





  


