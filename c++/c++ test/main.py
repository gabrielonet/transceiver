from time import sleep
import ctypes
lib = ctypes.CDLL('./test.so');
lib.start()

while True:
	x=lib.get_value()
	sleep(0.03)
	print x
