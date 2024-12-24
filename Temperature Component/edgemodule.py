import time
import fcntl as filelock
import threading
import subprocess

from ledmodule import start_warning_thread, update_threshold

#constants
LOCAL_THRESHOLD = 0
RAW_TEMP_DATA_FILE = "./datalogs/rawtemperaturedata.log"
THRESH_FILENAME = "./datalogs/thresholdconfiguration.log"
PROCESSED_DATA_FILE = "./datalogs/processedtemperaturedata.log"

def get_threshold(filename):
    """read the threshold setting from the file

    Args:
        filename (string): name of the file to read the data from

    Returns:
        float: the new threshold value
    """
    try:
        
        with open (filename, 'r') as file:
            filelock.flock(file, filelock.LOCK_SH)
            threshold = file.read().strip()
            filelock.flock(file, filelock.LOCK_UN)
            if (threshold != None):
                return float(threshold)
    except FileNotFoundError:
        return None
    except ValueError:
        print("Error unable to convert value to float")
        return None
    
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
    with open(PROCESSED_DATA_FILE, 'w') as file:
        if trend_detection:
            filelock.flock(file, filelock.LOCK_EX)
            file.write(f"Trend detected: All temmperatures below THRESHOLD in the last 30 seconds.\n")
            file.write(f"Temperatures detected: {temperatures}\n\n")
            file.flush()
            filelock.flock(file, filelock.LOCK_UN)
            


def trend_analysis(threshold, temperatures):
    """Analyses temperature data to detect downward trends

    Args:
        threshold (int): a value that determines the threshold
        temperatures (list): list of temperatures
    """
    print("current thrsh", threshold)
    start_warning_thread()
    
    if temperatures and all(temp < threshold for temp in temperatures):
        log_trend_analysis(True, temperatures)
        
        update_threshold(True)
    else:
        update_threshold(False)
        print("no trends detected")
    
    
    
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
        
        adjusted_thresh = get_threshold(THRESH_FILENAME)
        
        if adjusted_thresh:
            trend_analysis(adjusted_thresh, all_temperatures)
        else:
            trend_analysis(LOCAL_THRESHOLD, all_temperatures)


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