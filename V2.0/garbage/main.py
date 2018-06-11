
# import python stuff

import RPi.GPIO as GPIO
import time
from time import sleep
import os
from datetime import datetime

import Adafruit_ADS1x15


#import Kivy framework stuff
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.progressbar import ProgressBar
from kivy.uix.button import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.properties import NumericProperty,StringProperty,ReferenceListProperty,ObjectProperty
from kivy.lang import Builder


# Set up GPIO:
## define rotary encoder init setup
GPIO.setmode(GPIO.BCM)
encoderSwitch = 11
GPIO.setup(encoderSwitch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(14, GPIO.OUT)  # RF Preamp
GPIO.setup(26, GPIO.OUT)  # Sota mode selection
GPIO.setup(18, GPIO.OUT)  # Audio preamp
GPIO.setup(23, GPIO.OUT)  # Usb/Lsb


GPIO.output(14, 0)  # set RF Preamp to off ro RX
GPIO.output(26, 1)  # set Sota mode to Center
GPIO.output(18, 1)  # set Audio  Preamp to off 
GPIO.output(23, 0)  # set Cw/Usb 


encoder_temp = 0
freq =  open('/dev/shm/freq').read().rstrip()
freq = float(freq)
freq2 = "%08.5f" % (freq)
#offset = 8.001
offset = 9.0000845
step = 0.0001
tcvr_status = '[color=#008000]Rx[/color]'


class Main_Screen(FloatLayout):
        adc = Adafruit_ADS1x15.ADS1115()
        GAIN = 8
        value = NumericProperty()
        Svalue = NumericProperty()
        ceas = StringProperty()
        M1 = StringProperty()
        M2 = StringProperty()
        K1 = StringProperty()
        K2 = StringProperty()
        K3 = StringProperty()
        H1 = StringProperty()
        H2 = StringProperty()
        tcvr_status = StringProperty()
        af_preamp_status = StringProperty('[color=#008000]Off[/color]')
        rf_preamp_status = StringProperty('[color=#008000]Off[/color]')
        dsp_mode = StringProperty('Center Mode')
        rit_rx_status = StringProperty('Rit Off')
        rit_tx_status = StringProperty('Rit Off')
        rit_rx_bolean = False
        rit_tx_bolean = False
        rf_preamp_bolean = False
        af_preamp_bolean = False
        mode_bolean = False
        #mode_status = StringProperty()
        mode_status = StringProperty('Usb')
        sota_bolean = False
        band_switch_bolean = False
        rit = StringProperty()


        sota_bw = StringProperty()

        filter_start_x = NumericProperty()
        filter_stop_x = NumericProperty()
        sota_bw = StringProperty()
        sota_center = NumericProperty()
    	def update(self,a):
	    global freq2
	    #sota_center = 1750
	    while True:
	        sota_center_file = open('/dev/shm/sota_center').read().rstrip()
	        if  3 <= len(sota_center_file) <= 4:
	            sota_center = int(sota_center_file)
	            sota_bw_file = open('/dev/shm/sota_bw').read().rstrip()
	            break
	    if sota_bw_file != "":
			sota_bw = sota_bw_file
			self.filter_start_x = ((sota_center - int(sota_bw)/2)/10)
			self.filter_stop_x = ((sota_center + int(sota_bw)/2)/10)
			if self.filter_start_x < 200/10:
				self.filter_start_x = 200/10
			if self.filter_stop_x > 3500/10:
				self.filter_start_x = 3500/10
			
			


	    fifo1 = open('/dev/shm/freq').read().rstrip()
	    if fifo1 != "" : 
	        fifo = float(fifo1)-offset
                freq2 = "%08.5f" % (fifo)
                
                
            self.value = freq2
            self.M1 = str(freq2)[0:1]
            self.M2 = str(freq2)[1:2]
            self.K1 = str(freq2)[3:4]
            self.K2 = str(freq2)[4:5]
            self.K3 = str(freq2)[5:6]
            self.H1 = str(freq2)[6:7]
            self.H2 = str(freq2)[7:8]
            if step == 1:
                self.M2 = '[u]'+self.M2+'[/u]'
            if step == .1:
                self.K1 = '[u]'+self.K1+'[/u]'
            if step == .01:
                self.K2 = '[u]'+self.K2+'[/u]'
            if step == .001:
                self.K3 = '[u]'+self.K3+'[/u]'
            if step == .0001:
                self.H1 = '[u]'+self.H1+'[/u]'            
            if step == .00001:
                self.H2 = '[u]'+self.H2+'[/u]'   
            self.tcvr_status = tcvr_status
            self.ceas = datetime.now().strftime('%Y-%m-%d %H:%M')
            if tcvr_status == '[color=#008000]Rx[/color]' :
                self.rit = open('/dev/shm/rit_rx').read().rstrip()
            else: self.rit = open('/dev/shm/rit_tx').read().rstrip()
            # ADC converter is generating noise, temporary disabled
            self.Svalue = self.adc.read_adc(3, gain=self.GAIN) / 1
        def rit_rx(self):
	    self.rit_rx_bolean = not self.rit_rx_bolean
	    if self.rit_rx_bolean == True:
	       self.rit_rx_status = 'Rit On'
	       rit_status = open('/dev/shm/rit_rx_status','w')
               rit_status.write('on')
               rit_status.close()
	    else:
	       self.rit_rx_status = 'Rit Off'
	       rit = open('/dev/shm/rit_rx','w')
               rit.write('0.00')
	       rit_status = open('/dev/shm/rit_rx_status','w')
               rit_status.write('off')               
               rit.close()
               rit_status.close()


        def rit_tx(self):
	    self.rit_tx_bolean = not self.rit_tx_bolean
	    if self.rit_tx_bolean == True:
	       self.rit_tx_status = 'Rit On'
	       rit_status = open('/dev/shm/rit_tx_status','w')
               rit_status.write('on')               
	    else:
	       self.rit_tx_status = 'Rit Off'
	       rit = open('/dev/shm/rit_tx','w')
               rit.write('0.00')
               rit.close()              
               rit_status = open('/dev/shm/rit_tx_status','w')
               rit_status.write('off')               
               rit_status.close() 

        def rf_preamp(self):
			self.rf_preamp_bolean = not self.rf_preamp_bolean
			if self.rf_preamp_bolean == True:
				self.rf_preamp_status = '[color=#FF0000]On[/color]'
				GPIO.output(14, 1)
			else:
				GPIO.output(14, 0)
				self.rf_preamp_status = '[color=#008000]Off[/color]'

        def mode(self):
            self.mode_bolean = not self.mode_bolean
            if self.mode_bolean == False:
                self.mode_status = 'Usb'
                GPIO.output(23, 0)
            else:
                self.mode_status = 'Lsb'
                GPIO.output(23, 1)

        def af_preamp(self):
            self.af_preamp_bolean = not self.af_preamp_bolean
            if self.af_preamp_bolean == True:
                self.af_preamp_status = '[color=#FF0000]On[/color]'
                GPIO.output(18, 0)
            else:
                self.af_preamp_status = '[color=#008000]Off[/color]'
                GPIO.output(18, 1)


				


        def sota_mode(self):
            self.sota_bolean = not self.sota_bolean
            if self.sota_bolean == True:
                sota_write = open('/dev/shm/sota_mode','w').write('bw')
                GPIO.output(26, 0)
                sleep(0.1)
                GPIO.output(26, 1)
                self.dsp_mode = 'B/W Mode'     
            else:
                sota_write = open('/dev/shm/sota_mode','w').write('center')
                GPIO.output(26, 0)
                sleep(0.1)
                GPIO.output(26, 1)				
                self.dsp_mode = 'Center Mode'

        
        def band_switch(*kwargs):
          old_band = open('/dev/shm/band').read().rstrip()  
          
          if ( open('/dev/shm/tcvr_status').read().rstrip() == 'rx' and old_band not in kwargs[1:2] ) : 
            
            if   '3.5' in kwargs:
                band=3.5
            if   '7' in kwargs:
                band=7
            if   '14' in kwargs:
                band=14
            if   '21' in kwargs:
                band=21
            if   '28' in kwargs:
                band=28                
            new_band = open('/dev/shm/freq','w')
            new_band.write(repr(band+9.000097)) 
            new_old_band = open('/dev/shm/band','w')
            new_old_band.write(repr(band))
            new_band_tmp=band

                 
def xmit(*args):
             global tcvr_status
             if GPIO.input(11) == 0 :
		 tcvr_status = '[color=#FF0000]Tx[/color]'
		 tcvr = open('/dev/shm/tcvr_status','w')
                 tcvr.write('tx')               
             else  :  
                 tcvr_status = '[color=#008000]Rx[/color]'
		 tcvr = open('/dev/shm/tcvr_status','w')
                 tcvr.write('rx')             


                 
class MyApp(App):
      
	def build(self):
        
		# Set up the layout:
		layout = FloatLayout()
		# Instantiate  UI objects ):
                main_screen = Main_Screen()
		
		# Add the UI elements to the layout:
                #layout.add_widget(freq_display)
		layout.add_widget(main_screen)
		
		
                #GPIO.add_event_detect(17, GPIO.BOTH, callback=rotary)
                #GPIO.add_event_detect(18, GPIO.BOTH, callback=rotary)
                GPIO.add_event_detect(11, GPIO.BOTH, callback=xmit)

		#Clock.schedule_interval(freq_display.update, 0)
		
		Clock.schedule_interval(main_screen.update, 0)
                #Clock.schedule_once(shit)
		return layout

        
	def step_callback(obj, value):
	    global step
	    if ( value == 'right' and step > 0.00001) :
		  step = step / 10
		  step_file = open('/dev/shm/step','w')
		  step_file.write(repr(step))
	    if (value == 'left' and step < 1 ):
		  step = step * 10
		  step_file = open('/dev/shm/step','w')
		  step_file.write(repr(step))		  

if __name__ == '__main__':
	MyApp().run()

