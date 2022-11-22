import math
import re
from math import floor
from fractions import Fraction
import time
from time import *

freq = 7


    VCO = 900 # arbitrarry set at 900 Mhz
    ratio = VCO/freq
    M = floor(ratio)
    diff = ratio - M
    euclid = str(Fraction(diff))
    x = re.sub(r'/.*', '', str(euclid))
    y = re.sub(r'^.*?/', '', str(euclid))

    print (freq)
    print (M)
    print(x)
    print(y)
    freq = freq +1
