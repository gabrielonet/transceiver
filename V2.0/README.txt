Raspberry Pi default i2c bus is 100 Khz, so Python code will wait until si3531 gets updated by Rotary encoder.
	so encoder is useless over 100 grey codes per revolution if i2c bus speed  is not increased to 400 khz max (do not try 1Mhz ! trust me)
		edit /boot/config.txt and look for the line  dtparam=i2c_arm=on and replace with dtparam=i2c_arm=on,i2c_arm_baudrate=400000.
			Save it and reboot Rpi.In this way, I can use full 400 Grey codes optical encoder, for a 10 Hz resolution I can get about 4 Khz VFO / turn
			
			
			
			
			
