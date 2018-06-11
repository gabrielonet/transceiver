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
    #for vco in range(610,890):
    # div=int(vco/freq)
    # if (900 < div > 8 ): 
    #  break
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
    #print "compute freq = "+str(freq)
    si.setupPLL(si.PLL_A, a, b, c)
    if freq >= 37:
		level = 0x0F
    elif 30 <= freq <= 36.99999:
		level = 0x0E
    elif 23 <= freq <= 29.99999:
		level = 0x0D
    elif 1 <= freq <= 22.99999:
		level = 0x0C		
    si.setupMultisynth(0, si.PLL_A, div)
    si.enableOutputs(True)	    
    
# Generate 1 'st IF vxo
si = Si5351()
#si.setupPLL(si.PLL_B, 36, 0, 10)
#si.setupMultisynth(2, si.PLL_B, 100)


#si.enableOutputs(True)	        




## define rotary encoder init setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # VFO enc A
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP) # VFO enc B 

GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP) # tx switch

GPIO.setup(9, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP) # cw speed


GPIO.setup(16, GPIO.OUT) 
GPIO.setup(20, GPIO.OUT) 
GPIO.setup(21, GPIO.OUT) 
GPIO.setup(12, GPIO.OUT) 
GPIO.setup(13, GPIO.OUT) # Sota A
GPIO.setup(19, GPIO.OUT) # Sota B
GPIO.setup(26, GPIO.OUT) # Sota mode 
GPIO.setup(15, GPIO.OUT) # Sota reset


GPIO.output(12, 0)  # set TX/RX ro RX
GPIO.output(15, 0)  # Sota power off
sleep(1)
GPIO.output(15, 1)  # Sota Power on




if __name__=='__main__':
    rit_r_temp = 1
    rit_t_temp = 1
    rit_rx = 0
    rit_tx = 0
    band_relay=0
    freq =  open('/dev/shm/freq').read().rstrip()
    freq = float(freq)
    step = 0.00001
    #si = Si5351() 
    si.enableOutputs(True)
    integrat(freq)
    encoder_temp = 1
    mode_offset = 0.0005
    inter_freq = 9.000148
    #tcvr_state = 'rx'
    def rotary(greycode):
           freq =  open('/dev/shm/freq').read().rstrip()
           if freq != '' : 
               freq = float(freq)
           step = float(open('/dev/shm/step').read().rstrip())
           global encoder_temp
           global freq
           # detect if rotary right
           if (GPIO.input(17) == 0 and GPIO.input(4) == 1 and encoder_temp == 0):     # if port 25 == 1  
	      if freq <259.00001 :
                 freq +=step
                 fifo = open('/dev/shm/freq','w')
                 fifo.write(repr(freq))
                 fifo.close()
                 integrat(freq)
                 si_callback(freq=freq)
              encoder_temp = 1
           # Rearm  left / right detection   
           if (GPIO.input(17) == 1 and GPIO.input(4) == 1):  
              encoder_temp = 0 
           #detect rotary left   
           if (GPIO.input(17) == 1 and GPIO.input(4) == 0 and encoder_temp == 0):     # if port 25 == 1  
              if freq > 0.10000 : 
                 freq -=step
                 fifo = open('/dev/shm/freq','w')
                 fifo.write(repr(freq))
                 fifo.close()
                 integrat(freq)
                 si_callback(freq=freq)
              encoder_temp = 1 



           
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
		      si_callback(rit_rx=rit_rx)
		    
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
			si_callback(rit_rx=rit_rx)
		  
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
		      si_callback(rit_tx=rit_tx)
		    
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
			si_callback(rit_tx=rit_tx)


    sota_temp = 0		
    sota_center = 1500
    sota_bw = 2400
    
    def sotabeam(greycode):
        global sota_temp
        global sota_bw
        global sota_center
        sota_mode = open('/dev/shm/sota_mode','r').read().rstrip()
        # detect if rotary right
        sota_sleep = 0.03
        if sota_mode == 'bw':   
            if (GPIO.input(10) == 0 and GPIO.input(9) == 1 and sota_temp == 0):

                   if 3500 > sota_bw >= 700:
                       sota_bw +=100
                   elif 700 > sota_bw >= 400:
                       sota_bw +=50
                   elif 400 > sota_bw >= 200 : 
                       sota_bw +=20               
                   sota_temp = 1
                   sota_bw_file = open('/dev/shm/sota_bw','w')
                   sota_bw_file.write(repr(sota_bw))
                   sota_bw_file.close()
                   GPIO.output(19, 1)
                   sleep(sota_sleep)
                   GPIO.output(13, 1)
                   sleep(sota_sleep)
                   GPIO.output(13, 1)
                   sleep(sota_sleep)
                   GPIO.output(19, 0)
                   sleep(sota_sleep)
                   GPIO.output(13, 0)
                   
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
                   sota_bw_file = open('/dev/shm/sota_bw','w')
                   sota_bw_file.write(repr(sota_bw))
                   sota_bw_file.close()
                   GPIO.output(13, 1)
                   sleep(0)
                   GPIO.output(19, 1)
                   sleep(sota_sleep)
                   GPIO.output(13, 1)
                   sleep(sota_sleep)
                   GPIO.output(13, 0)
                   sleep(sota_sleep)
                   GPIO.output(19, 0)
                   
        if sota_mode == 'center':   
            if (GPIO.input(10) == 0 and GPIO.input(9) == 1 and sota_temp == 0):

                   if 3500 > sota_center >= 2000:
                       sota_center +=50
                   elif 2000 > sota_center:
                       sota_center +=25
                   sota_temp = 1
                   sota_center_file = open('/dev/shm/sota_center','w')
                   sota_center_file.write(repr(sota_center))
                   sota_center_file.close()
                   GPIO.output(19, 1)
                   sleep(0.01)
                   GPIO.output(13, 1)
                   sleep(0.01)
                   GPIO.output(13, 1)
                   sleep(0.01)
                   GPIO.output(19, 0)
                   sleep(0.01)
                   GPIO.output(13, 0)
                   
            # Rearm  left / right detection   
            if (GPIO.input(9) == 1 and GPIO.input(10) == 1):  
              sota_temp = 0 
            #detect rotary left   
            if (GPIO.input(10) == 1 and GPIO.input(9) == 0 and sota_temp == 0):     # if port 25 == 1  

                   if sota_center >= 2001:
                       sota_center -=50
                   elif 2000 >= sota_center > 200:
                       sota_center -=25
                  
                   sota_temp = 1
                   sota_center_file = open('/dev/shm/sota_center','w')
                   sota_center_file.write(repr(sota_center))
                   sota_center_file.close()
                   GPIO.output(13, 1)
                   sleep(0.01)
                   GPIO.output(19, 1)
                   sleep(0.01)
                   GPIO.output(13, 1)
                   sleep(0.01)
                   GPIO.output(13, 0)
                   sleep(0.01)
                   GPIO.output(19, 0)                   
        
			

    def xmit(*args):
       freq =  open('/dev/shm/freq').read().rstrip()
       freq = float(freq)
       mode_offset = 0.0005
       inter_freq = 9
       rit_r = open('/dev/shm/rit_rx').read().rstrip()
       rit_t = open('/dev/shm/rit_tx').read().rstrip()
       if  GPIO.input(11) == 0 :
            print freq
            print inter_freq
            integrat(freq-inter_freq)
            GPIO.output(12, 1) 
       else:
			integrat(freq)
			GPIO.output(12, 0) 
    def si_callback(**kwargs):
		global freq
		global rit_rx
		global rit_tx
		if 'freq' in kwargs:
			freq = kwargs['freq']
		if 'rit_rx' in kwargs:
			rit_rx = kwargs['rit_rx']
		if 'rit_tx' in kwargs:
			rit_tx = kwargs['rit_tx']			
		rit_r ="%0.2f" % Decimal(rit_rx)
		rit_t ="%0.2f" % Decimal(rit_tx)
		si_freq = float(rit_r) + freq

    GPIO.add_event_detect(4, GPIO.BOTH, callback=rotary)
    GPIO.add_event_detect(17, GPIO.BOTH, callback=rotary)
    GPIO.add_event_detect(22, GPIO.BOTH, callback=clarifier)
    GPIO.add_event_detect(27, GPIO.BOTH, callback=clarifier)
    GPIO.add_event_detect(11, GPIO.BOTH, callback=xmit)
    GPIO.add_event_detect(10, GPIO.BOTH, callback=sotabeam)
    GPIO.add_event_detect(9 , GPIO.BOTH, callback=sotabeam)    
    try:
     while True:
      global band_relay   
      sleep(1)
      freq_relays =  open('/dev/shm/freq', 'r').read().rstrip()
      status_relays =  open('/dev/shm/tcvr_status', 'r').read().rstrip()
      if  [ freq_relays != '' and status_relays != '' ]:
        if status_relays == "rx":
           band2=float(freq_relays)-9      
           if 0 <= band2 <= 5:
               GPIO.output(16, 1)       # set port/pin value to 1/GPIO.HIGH/True  
               GPIO.output(20, 0) 
               GPIO.output(21, 0) 
               band_relays=3.5
           elif  5 <= band2 <= 9:
               GPIO.output(16, 0)       # set port/pin value to 1/GPIO.HIGH/True  
               GPIO.output(20, 1) 
               GPIO.output(21, 0) 
               band_relays=7 
           elif  9 <= band2 <= 18:
               GPIO.output(16, 1)       # set port/pin value to 1/GPIO.HIGH/True  
               GPIO.output(20, 1) 
               GPIO.output(21, 0)
               band_relays=14
           elif  18 <= band2 <= 24:
               GPIO.output(16, 0)       # set port/pin value to 1/GPIO.HIGH/True  
               GPIO.output(20, 0) 
               GPIO.output(21, 1)
               band_relays=21
           elif  24 <= band2 <= 30:
               GPIO.output(16, 1)       # set port/pin value to 1/GPIO.HIGH/True  
               GPIO.output(20, 0) 
               GPIO.output(21, 1)
               band_relays=28
           
           if band_relay != band_relays :
               integrat(float(freq_relays))
               band_relay=band_relays
               print 'am schimbat releele pentru banda de '+str(band_relays)




    except KeyboardInterrupt:
           print "good by yo8rxp"
           GPIO.cleanup()       # clean up GPIO on CTRL+C exit
    GPIO.cleanup()           # clean up GPIO on normal exit





  


