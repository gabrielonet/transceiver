def comm_transmision(dummy,freq):
          
            import serial
            from serial import Serial
            from time import sleep
            serialport="/dev/ttyUSB0"  
            ser = serial.Serial(serialport, 9600)
            y=""
            while True :
                freq_len=len(str(int(freq.value*10)))
                if freq_len <3 :
                    serial_freq = str("0" + str(int(freq.value*10)))
                else:
                    serial_freq = str(int(freq.value*10))
                x =  ser.read()
                if x != ";":
                    disp = str(y)+str(x)
                    y=disp
                else:
                    y = ""
                    ##ser.write("IF00014175000     +999000000130000000;")
                if disp == "FA":
                    ser.write("FA000" + str(serial_freq)+"00000;")
                sleep(0.1)    
                
            
        
