import socket
import time
import fcntl as filelock
import threading
import subprocess


THRESHOLD = 2
RAW_TEMP_DATA_FILE = "temperaturelog"
PROCESSED_TEMP_DATA_FILE = "processeddata.log"


#initiate the sensor
def call_sensormodule():
    subprocess.call(["python3", "sensormodule.py"])
    
def call_clientmodule():
    subprocess.call(["python3", "clientmodule.py"])

#read the temperatue file
def read_raw_temp_data(filename):
    while True:
        try:
            with open(filename, "r") as file:
                filelock.flock(file, filelock.LOCK_SH)
                
                lines = file.readlines()
                
                filelock.flock(file, filelock.LOCK_UN)
            
            if lines:
                for line in reversed(lines):
                    if "Temperature" in line:
                        temp = float(line.split(":")[1].strip("°C\n"))
                        return temp
            return None
            
        except FileNotFoundError :
            quit()


def log_trend_analysis(filename, trend_detection, temperatures):
    with open(filename, 'a') as file:
        if trend_detection:
            file.writelines(f"Trend detected: All temmperatures below {THRESHOLD} in the last 30 seconds.\n")
            file.writelines(f"Temperatures detected: {temperatures}\n\n")
            file.flush()

#data processing
def process_temperature():
    while True:
        all_temperatures = []
        
        start_time = time.time()
        while time.time() - start_time < 30:
            temperature = read_raw_temp_data(RAW_TEMP_DATA_FILE)
            if temperature is not None:
                all_temperatures.append(temperature)
            time.sleep(3) #query the data every 3 seconds
        

        if all_temperatures and all(temp < THRESHOLD for temp in all_temperatures):
            triggerActuator(True)
            log_trend_analysis(PROCESSED_TEMP_DATA_FILE, True, all_temperatures)
        else:
            print(f"Everything is fine")
            triggerActuator(False)
            
            

def triggerActuator(value):
    if(value):
        print("Actuactor must be functional now")
    else:
        print("Actuator is off")


def main():
    sesnorthread = threading.Thread(target=call_sensormodule)
    clientthread = threading.Thread(target=call_clientmodule)
    try:
         sesnorthread.start()
         clientthread.start()
    except:
        print("failed to start sensor or client")
        
    process_temperature()
    
if __name__ == '__main__':
    main()