import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setmode (GPIO.BCM)
GPIO.setwarnings(False)
pin_A = 4
pin_B = 17
GPIO.setup (pin_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)         # pin input pullup
GPIO.setup (pin_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)         # pin input pullup


a_state = GPIO.input(pin_A)
b_state = GPIO.input(pin_B)
temp_a = a_state
temp_b = b_state
counter = 0


Encoder_Count = 0

def enc_a(dummy):
    global a_state
    global b_state
    a_state = not  a_state
    enc_compute(a_state,b_state)

def enc_b(dummy):
    global a_state
    global b_state
    b_state = not  b_state
    enc_compute(a_state,b_state)
        
def enc_compute(a_state,b_state):
    global temp_a,temp_b,counter
    if ( temp_a == 0 and temp_b == 0 and a_state == 1):
        counter -=1
    if ( temp_a == 0 and temp_b == 0 and b_state == 1):
        counter +=1        
 
    print "counter"+str(counter)
    temp_a = a_state
    temp_b = b_state


GPIO.add_event_detect (pin_A, GPIO.BOTH, callback=enc_a)   # Enable interrupt
GPIO.add_event_detect (pin_B, GPIO.BOTH, callback=enc_b)


while(1):
	sleep(1)
