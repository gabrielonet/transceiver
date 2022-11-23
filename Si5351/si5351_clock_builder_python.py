print ("Start")
import time
import math
import re
from math import floor
import time
from time import sleep
freq = round(7.00001, 5)        ### in Mhz
#freq = 7.000123 ### in Mhz

multisynth_divider = 100 # define static multisynth divider for Freq out in range of 6 to 9 Mhz since VCO freq = Freq out x Multisynth. TO BE FIXED !!
VCO = freq * multisynth_divider
#### So, in case of 7 Mhz output, we need a 700Mhz VCO and a multisynth divider = 100
#### Now we need to set VCO freq
crystal = 25 ### Some models have 27 Mhz crystals inside, mine has 25 Mhz
##   VCO = 25 x (a+b/c)  , where 25 is Crystal oscillator and we need to get a, b and c values
##   As an example , if VCO = 700 then a+b/c = 700/25 =28
##   In this ideal case, we can set a=28 . then b/c = 0 as b=0 and c =1
fractional_value = VCO / crystal
###  If fractional_value is not idealy integer, then we should make a = lowest integer part and compute difference
a = floor(fractional_value)
diff = fractional_value - a
diff = f"{diff:.5f}"
####   So far we got VCO , multisynth_divider, and fractional_value. From fractional value we got a, b and c values if fractional value is integer (ideal)
###    Now it is time to get b and c values knowing te result of b/c. How that since multiple values are possible ? Using reverse Euclid, we need to determine
###    first combination of B and C , not all combinations !!
###    We got to import Fraction from fractions, and that library will give us those 2 values. But Rasppberry Pi Pico does not have this class.
###    Let's make it more simple !!! Any  floating point number can be represented by an integer divided by 10^x. In this case, we compute decimal part
###    lenght and multiply it with 10^lenght

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
print("Now we can write I2C registries with above values")
print ("To be continued.......")
   
