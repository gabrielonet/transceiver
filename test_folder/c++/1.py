from time import sleep
import ctypes
lib = ctypes.CDLL('./test.so');
x=lib
print x

