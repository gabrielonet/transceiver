def comm_transmision(dummy,freq):
          
            import serial
            from serial import Serial
            from time import sleep
            y=""
            ser = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
            )
                
            while True :

                freq_len=len(str(int(freq.value*10)))
                if freq_len <3 :
                    serial_freq = str("0" + str(int(freq.value*10)))
                else:
                    serial_freq = str(int(freq.value*10))
                ser.write("IF00014175000     +999000000130000000;")
                ser.write("FA000"+str(serial_freq)+"00000;")
                     
                    
                
         