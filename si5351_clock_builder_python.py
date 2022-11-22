#!/usr/bin/python
import math
import re
from math import floor
from fractions import Fraction
import time
from time import *

## SI5351 is based on 4 unknown values equation. So it is impossible resolving it if not using some predetermined values
## This is where most of users fail to generate propper values, if using bad written ino sketchups then great jitter on output
## SI5351 DO like integer values, not decimals on dividers

freq = 7.000123 ### in Mhz
### VCO in range of 600 - 900 Mhz 
multisynth_divider = 100 # define static multisynth divider for Freq out in range of 6 to 9 Mhz since VCO freq = Freq out x Multisynth 
VCO = freq * multisynth_divider
####  So, in case of 7 Mhz output, we need a 700Mhz VCO and a multisynth divider = 100
#### Now we need to set VCO freq


crystal = 25 ### Some models have 27 Mhz crystals inside, mine has 25 Mhz

##   VCO = 25 x (a+b/c)  , where 25 is Crystal oscillator and we need to get a, b and c values
## As an example , if VCO = 700 then a+b/c = 700/25 =28
## In this ideal case, we can set a=28 . then b/c = 0 as b=0 and c =1


fractional_value = VCO / crystal

###  If fractional_value is not idealy integer, then we should check this, make a = lowest integer part and compute difference


if (fractional_value.is_integer()) :
    print ("Fractional value is integer")
    a = int(fractional_value)
    b = 0
    c = 1
    diff = 0

####   So far we got VCO , multisynth_divider, and fractional_value. From fractional value we got a, b and c values if fractional value is integer (ideal)
###    Now it is time to get b and c values knowing te result of b/c. How that since multiple values are possible ? Using reverse Euclid, we need to determine first a and b set , not all !!
###    We got to import Fraction from fractions, and that library will give us those 2 values    

else:
    print ("Fractional value nu este integer")
    a = floor(fractional_value)
    diff = fractional_value - a     
    euclid = str(Fraction(diff))
    a = re.sub(r'/.*', '', str(euclid))
    b = re.sub(r'^.*?/', '', str(euclid))



print("Freq = " + str(freq) + "Mhz")
print("VCO = " + str(VCO)+"Mhz")
print("Multisynth divider = " + str(multisynth_divider))
print("fractional value = " + str(fractional_value))
print ("a = "+ str(a))
print ("b= "+ str(b))
