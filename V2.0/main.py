#!/usr/bin/python
from __future__ import division

import time
import os
from time import sleep
from datetime import datetime
from ctypes import c_char_p
from decimal import Decimal
import math


import multiprocessing
from multiprocessing import Process, Value
import RPi.GPIO as GPIO

import Adafruit_ADS1x15
#import Adafruit_MCP4725



import encoder
import dsp
import comm
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
import math
from math import floor
import fractions
from fractions import Fraction
from Si5351 import Si5351 
si = Si5351()





#GPIO.cleanup()  
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)  # RF Preamp
GPIO.setup(20, GPIO.OUT)  # Audio preamp
GPIO.setup(23, GPIO.OUT)  # Usb
GPIO.setup(25, GPIO.OUT)  # Lsb
GPIO.setup(8, GPIO.OUT)  # CW
GPIO.setup(16, GPIO.OUT)  #  AGC_mode
GPIO.output(16, 0)  #  Set AGC to auto



GPIO.output(24, 0)  # set RF Preamp to off ro RX
GPIO.output(13, 1)  # set Sota mode to Center
GPIO.output(20, 1)  # set Audio  Preamp to off 
GPIO.output(23, 1)  # set USB on
GPIO.output(25, 0)  # set LSB off
GPIO.output(8, 0)  # set CW off
GPIO.output(20, 0)


class Main_Screen(FloatLayout):
        #dac = Adafruit_MCP4725.MCP4725(address=0x61, busnum=1)
        adc = Adafruit_ADS1x15.ADS1115()
        GAIN = 1
        meter = 0
        power = 0
        utc_time = StringProperty()
        M1 = StringProperty()
        M2 = StringProperty()
        K1 = StringProperty()
        K2 = StringProperty()
        K3 = StringProperty()
        H1 = StringProperty()
        H2 = StringProperty()
        button_image  = StringProperty()
        last_mode = 23

       

        meter = NumericProperty()
        power = NumericProperty()
        af_preamp_bolean = False
        af_preamp_status = StringProperty('[color=#008000]Off[/color]')
        rf_preamp_bolean = False
        full_break_bolean = False
        rf_preamp_status = StringProperty('[color=#008000]Off[/color]')
        full_break_status = StringProperty('[color=#008000]Off[/color]')
        
        mode_bolean = False
        mode_status = StringProperty('Usb')
        agc_status = StringProperty('Auto')
        sota_bolean = False
        agc_bolean = True

        dsp_mode = StringProperty('Center Mode')
        tcvr_status = StringProperty()
        agc_mode = NumericProperty()
        rit_rx_status = StringProperty('Rit Off')
        rit_tx_status = StringProperty('Rit Off')
        rit_rx_bolean = False
        rit_tx_bolean = False
        band_switch_bolean = False
        rit = StringProperty()
        sota_bw = StringProperty()
        filter_start_x = NumericProperty()
        filter_stop_x = NumericProperty()
        sota_bw = StringProperty()
        sota_center = NumericProperty()
        speed = NumericProperty()
        mode_usb=StringProperty('[color=#FF0000]' + "USB" + '[/color]')
        mode_usbcw=StringProperty("USB+CW")
        mode_lsb=StringProperty("LSB")
        

        
        
        
        def rf_preamp(self):
            self.rf_preamp_bolean = not self.rf_preamp_bolean
            if self.rf_preamp_bolean == True:
                self.rf_preamp_status = '[color=#FF0000]On[/color]'
                GPIO.output(24, 1)
            else:
                GPIO.output(24, 0)
                self.rf_preamp_status = '[color=#008000]Off[/color]'

        def mode(self,mode_value):
            if mode_value == 23:
                GPIO.output(self.last_mode, 0)
                GPIO.output(23, 1)
                self.last_mode = 23
                self.mode_usb= '[color=#FF0000]' + "USB" + '[/color]'
                self.mode_usbcw= 'USB+CW'
                self.mode_lsb= 'LSB'

            if mode_value == 25:
                GPIO.output(self.last_mode, 0)
                GPIO.output(25, 1)
                self.last_mode = 25
                self.mode_usb= 'USB'
                self.mode_usbcw= 'USB+CW'
                self.mode_lsb= '[color=#FF0000]' + "LSB" + '[/color]'             
                
            if mode_value == 8:
                GPIO.output(self.last_mode, 0)                
                GPIO.output(8, 1)
                self.last_mode = 8 
                self.mode_usb= 'USB'
                self.mode_usbcw= '[color=#FF0000]' + "USB+CW" + '[/color]'
                self.mode_lsb= 'LSB'
                
            touch_event.value = int('3'+ str(self.last_mode))    
            #print self.last_mode    

        def agc(self):
            self.agc_bolean = not self.agc_bolean
            if self.agc_bolean == True:
                self.agc_status = 'Auto'
                self.agc_mode = 1
                GPIO.output(16,0)

                
            else:
                self.agc_status = 'Manual ->'
                self.agc_mode = 0
                GPIO.output(16,1)


        def sys_shut_down(arg):
            os.system("shutdown now -h")
        def sys_reboot(arg):
            os.system("reboot")            
        

        def af_preamp(self):
            self.af_preamp_bolean = not self.af_preamp_bolean
            if self.af_preamp_bolean == True:
                self.af_preamp_status = '[color=#FF0000]On[/color]'
                GPIO.output(20, 0)
                af_pre.value = 1
            else:
                self.af_preamp_status = '[color=#008000]Off[/color]'
                GPIO.output(20, 1)
                af_pre.value = 0

        def rit_rx(self):
            self.rit_rx_bolean = not self.rit_rx_bolean
            if self.rit_rx_bolean == True:
                rit_rx.value = 1
            else:
                rit_rx.value = 0
                rit.value = 0
            touch_event.value = 1 

        def rit_tx(self):
            self.rit_tx_bolean = not self.rit_tx_bolean
            if self.rit_tx_bolean == True:
                rit_tx.value = 1
            else:
                rit_tx.value = 0
                rit.value = 0
        def slider(self,slider_value):
             speed.value  = int(slider_value)

        def step_callback(obj, arrow):
            if ( arrow == 'right' and step.value > 0.00001) :
                step.value = step.value / 10
            if (arrow == 'left' and step.value < 1 ):
                step.value = step.value * 10
        def sota_mode(self):
            self.sota_bolean = not self.sota_bolean
            if self.sota_bolean == True:
                GPIO.output(13, 0)
                sleep(0.1)
                GPIO.output(13, 1)
                self.dsp_mode = 'B/W Mode'
                sota_dsp_mode.value = 0
            else:
                GPIO.output(13, 0)
                sleep(0.1)
                GPIO.output(13, 1)              
                self.dsp_mode = 'Center Mode'
                sota_dsp_mode.value = 1
        def band_switch(dummy,band):
            touch_event.value = int('2'+band)
        
        
        def full_break(self):
            self.full_break_bolean = not self.full_break_bolean
            if self.full_break_bolean == True:
                self.full_break_status = '[color=#FF0000]On[/color]'
                full_break.value = 1
            else:
                self.full_break_status = '[color=#008000]Off[/color]'
                full_break.value = 0 


        def update(self,*args):
            global start_freq
            global band_tmp
            freq2 = "%08.5f" % (freq.value)
            self.M1 = str(freq2)[0:1]
            self.M2 = str(freq2)[1:2]
            self.K1 = str(freq2)[3:4]
            self.K2 = str(freq2)[4:5]
            self.K3 = str(freq2)[5:6]
            self.H1 = str(freq2)[6:7]
            self.H2 = str(freq2)[7:8]
            ##########  Band  Relay update  ##############   
            if int(str(self.M1)+str(self.M2)) != band_tmp:
                if 0 <= int(str(self.M1)+str(self.M2)) <=5:
                        GPIO.output(14, 0)  
                        GPIO.output(15, 0) 
                        GPIO.output(18, 0)
                        button_image = "img/shape_off.png"
                        #self.dac.set_voltage(1265)
                        band_tmp = 3.5
                if 5 < int(str(self.M1)+str(self.M2)) <=9:
                        GPIO.output(14, 1)  
                        GPIO.output(15, 0) 
                        GPIO.output(18, 0)
                        #self.dac.set_voltage(1271)
                        band_tmp = 7
                if 9 < int(str(self.M1)+str(self.M2)) <=18:
                        GPIO.output(14, 0)  
                        GPIO.output(15, 1) 
                        GPIO.output(18, 0) 
                        #self.dac.set_voltage(1300)
                        band_tmp = 14
                if 18 < int(str(self.M1)+str(self.M2)) <=24:
                        GPIO.output(14, 1)  
                        GPIO.output(15, 1) 
                        GPIO.output(18, 0)
                        #self.dac.set_voltage(1495)
                        band_tmp = 21
                if 24 < int(str(self.M1)+str(self.M2)) <=30:
                        GPIO.output(14, 0)  
                        GPIO.output(15, 0) 
                        GPIO.output(18, 1)
                        #self.dac.set_voltage(1530)
                        band_tmp = 28
                #print int(str(self.M1)+str(self.M2))
                #print band_tmp
            if step.value == 1:
                self.M2 = '[color=#FF0000]'+self.M2+'[/color]'
            if step.value == .1:
                self.K1 = '[color=#FF0000]'+self.K1+'[/color]'
            if step.value == .01:
                self.K2 = '[color=#FF0000]'+self.K2+'[/color]'
            if step.value == .001:
                self.K3 = '[color=#FF0000]'+self.K3+'[/color]'
            if step.value == .0001:
                self.H1 = '[color=#FF0000]'+self.H1+'[/color]'            
            if step.value == .00001:
                self.H2 = '[color=#FF0000]'+self.H2+'[/color]'               
            self.utc_time = str(datetime.now().strftime('%Y-%m-%d %H:%M'))
            self.rit = str("%0.2f" % Decimal(rit.value*1000))
            if tcvr_status.value == 0:
                self.tcvr_status = '[color=#008000]Rx[/color]'
            else:
                self.tcvr_status = '[color=#FF0000]Tx[/color]'
                
            ### DSP UPDATE ###
            self.filter_start_x = dsp_start_x.value/10
            self.filter_stop_x = dsp_stop_x.value/10
            ## ADC converter
            #self.meter = int(self.adc.read_adc(2, gain=self.GAIN))
            #speed.value = int(self.adc.read_adc(0, gain=self.GAIN))
            self.power = int(self.adc.read_adc(3, gain=8))
            #print self.power
            self.meter = (26000-self.power)/140

class MyApp(App):
      
    def build(self):
        # Set up the layout:
        layout = FloatLayout()
        #Instantiate  UI objects ):
        main_screen = Main_Screen()
        # Add the UI elements to the layout:
        layout.add_widget(main_screen)
        Clock.schedule_interval(main_screen.update, 0.03)
        return layout
if __name__ == '__main__':
    start_freq =14
    #band_tmp = start_freq
    band_tmp=0
    freq = Value('d', start_freq)
    step = Value('d',0.0001)
    bfo = Value('d',0)
    tcvr_status = Value('i',0 )
    af_pre = Value('i',1)
    rit = Value('d',0 )
    rit_rx = Value('i',0 )
    rit_tx = Value('i',0 )
    speed = Value('i',0 )
    full_break = Value('i', 0)
    dsp_start_x = Value('i', 200)
    dsp_stop_x = Value('i' , 3500)
    sota_dsp_mode = Value('i' , 1) 
    touch_event = Value('i',int('2'+str(start_freq)) )   
    proc_1 = multiprocessing.Process(target=encoder.buttons , args = (freq,step,tcvr_status,rit,rit_rx,rit_tx,touch_event,af_pre,bfo,full_break) )
    proc_1.start()
    proc_2 = multiprocessing.Process(target=dsp.sota_dsp , args = (sota_dsp_mode,dsp_start_x,dsp_stop_x) )    
    proc_2.start()
    proc_3 = multiprocessing.Process(target=comm.comm_transmision , args = (1, freq))
    proc_3.start()
    MyApp().run()
    
   

    ######## LEGEND ######
    # 1x - rit events
    # 2x - band events
    # 3x - mode events
    

