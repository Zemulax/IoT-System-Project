import socket
import time
import fcntl as filelock
import threading
import subprocess

from ledmodule import start_warning_thread

#constants
THRESHOLD = 200
RAW_TEMP_DATA_FILE = "temperaturelog"



def call_sensormodule():
    """calls the sensor as a subprocess
    """
    subprocess.call(["python3", "sensormodule.py"])
    
def call_clientmodule():
    """calls clientmodule as a subprocess
    """
    subprocess.call(["python3", "clientmodule.py"])

def call_ledmodule():
    """calls led module
    """
    subprocess.call(["python3", "ledmodule.py"])

def read_raw_temp_data(filename):
    """reads temperature data from the temperature log file
       uses locking mechanism
       extracts the temperature value from the reading

    Args:
        filename (string): the file to read data from

    Returns:
        _float_: temperature value in float
    """
    while True:
        try:
            with open(filename, "r") as file:
                filelock.flock(file, filelock.LOCK_SH) #lock the file
                
                lines = file.readlines()
                
                filelock.flock(file, filelock.LOCK_UN) #unlock the file
            
            if lines:
                for line in reversed(lines):
                    if "Temperature" in line:
                        temp = float(line.split(":")[1].strip("°C\n"))
                        return temp
            return None
            
        except FileNotFoundError :
            quit()


def log_trend_analysis( trend_detection, temperatures):
    """

    Args:
        filename (string): name of the file to write trends to
        trend_detection (bool): dichotomy of trends
        temperatures (list): list of data thats creating a negative trend
    """
    with open("processeddata.log", 'a') as file:
        if trend_detection:
            file.writelines(f"Trend detected: All temmperatures below {THRESHOLD} in the last 30 seconds.\n")
            file.writelines(f"Temperatures detected: {temperatures}\n\n")
            file.flush()


def trend_analysis(threshold, temperatures):
    """Analyses temperature data to detect downward trends

    Args:
        threshold (int): a value that determines the threshold
        temperatures (list): list of temperatures
    """
    
    if temperatures and all(temp < threshold for temp in temperatures):
        log_trend_analysis(True, temperatures)
        start_warning_thread(True)
    else:
        start_warning_thread(False)
    
    
    
def process_temperature():
    """initiates temperature data collection over a specified period of time
       analyses temperature data to detect negative threshold trends.
       if trends are detected they are recored
    """
    while True:
        all_temperatures = []
        
        start_time = time.time()
        while time.time() - start_time < 30:
            temperature = read_raw_temp_data(RAW_TEMP_DATA_FILE)
            if temperature is not None:
                all_temperatures.append(temperature)
            time.sleep(3) #query the data every 3 seconds
            
        #process temperature data once collection done
        trend_analysis(THRESHOLD, all_temperatures)
            
            
#awaiting full implementation
def triggerActuator(value):
    """triggers an actuator as a response to trend analysis
    Args:
        value (_type_): _description_
    """
    start_warning_thread(value)


def main():
    """calls all functions
    """
    sensorthread = threading.Thread(target=call_sensormodule)
    clientthread = threading.Thread(target=call_clientmodule)
    try:
         sensorthread.start()
         clientthread.start()
    except:
        print("failed to start sensor or client")
        
    process_temperature()
    
if __name__ == '__main__':
    main()