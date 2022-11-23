print ("Start")
import time
import math
import re
from math import floor
import time
from time import sleep
freq = round(7.00000, 5)        ### in Mhz
#freq = 7.000123 ### in Mhz

multisynth_divider = 100 # define static multisynth divider for Freq out in range of 6 to 9 Mhz since VCO freq = Freq out x Multisynth 
VCO = freq * multisynth_divider
crystal = 25 ### Some models have 27 Mhz crystals inside, mine has 25 Mhz
fractional_value = VCO / crystal
a = floor(fractional_value)
diff = fractional_value - a
diff = f"{diff:.5f}"
integer_part = re.sub(r'\..*', '', str(diff))
decimal_part = re.sub(r'.*\.', '', str(diff))
decimal_lenght = len (decimal_part)
b = int(decimal_part)
c = int(math.pow(10, decimal_lenght))
print("Freq = " + str(freq) + " Mhz")
print("VCO = " + str(VCO)+"  Mhz")
print("Multisynth divider = " + str(multisynth_divider))
print("fractional value = " + str(fractional_value))
print ("a = "+ str(a))
print ("b= "+ str(b))
print ("c= "+ str(c))
