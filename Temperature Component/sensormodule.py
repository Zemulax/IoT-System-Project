#libraries
import board
import adafruit_dht
import time
import fcntl as filelock


print("SENSOR INITIATED")
#constants
FILENAME = "temperaturelog"
PIN_NUMBER = board.D4
HEADER = "Temperature Recordings\n\n"

#variables
dhtSensor = adafruit_dht.DHT11(PIN_NUMBER) #initialize the sensor
line_number = 2

#read temperature from the sensor
#write the values to an external file
    
def errorLogger(error):
    with open("temperaturelog", 'w') as file:
        file.truncate()
        file.write(error)
        file.flush()

def read_temperature():
    with open(FILENAME, 'w+') as file:
        
        lines = file.readlines() #read file lines
        
        if not lines:
            lines.append(HEADER)
            
            while True:
                try:
                        filelock.flock(file, filelock.LOCK_SH)
                        
                        #assign temp reading to variables
                        temperature_c = dhtSensor.temperature
                        
                        if len(lines) >= line_number:
                            lines [line_number-1] = f"Temperature: {temperature_c:.1f} °C\n"
                        else:
                            lines.append(f"Temperature:{temperature_c:.1f} °C\n")
                        
                        file.seek(0) #get back to the file start
                        file.writelines(lines) #write to the file
                        filelock.flock(file, filelock.LOCK_UN) #unlcok the file
                        file.truncate() #delete rest of the file
                        file.flush() #flush the buffer
                        time.sleep(40.0)
                        
                
                except  RuntimeError as error:
                        errorLogger("awaiting Sensor...")
                        time.sleep(30)
                        continue
                
                except  TypeError:
                        file.write("Unable tyo read from sensor")
                        time.sleep(10)
                        continue
                
                except  OverflowError:
                        errorLogger("Halted. Connect the sensor and Restart the program")
                        time.sleep(20)
                        quit()
                                
        
        dhtSensor.exit()
    

def main():
    read_temperature()
    
if __name__ == "__main__":
    main()