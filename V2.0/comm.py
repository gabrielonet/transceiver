def comm_transmision(dummy,freq):
          
            import serial
            from serial import Serial
            y=""
            serialport = "/dev/ttyUSB0"
            ser = serial.Serial(serialport, 9600)
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
                if disp == "FA":
                    ser.write("FA000" + str(serial_freq)+"00000;")
                    print "Disp = "+str(disp)
                    print 'sending FA'     
                    