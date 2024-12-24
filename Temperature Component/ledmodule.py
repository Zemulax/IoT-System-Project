import RPi.GPIO as GPIO # type: ignore
import time
import threading

#constants
LED_PIN = 23
LED_PINB = 16

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(LED_PINB, GPIO.OUT)

threshold_exceeded = threading.Event()


def temp_threshold_warning():
    """triggers actuator in response to edge module data analysis

    Args:
        threshold_exceeded (bool): whether the actuator should be on or off
    """
    
    try:
        while True:
            if threshold_exceeded.is_set():
                GPIO.output(LED_PIN, GPIO.HIGH)
                time.sleep(3)
                
                GPIO.output(LED_PIN, GPIO.LOW)
                time.sleep(3)
            else:
                #turn green LED on
                GPIO.output(LED_PINB, GPIO.HIGH)
    except KeyboardInterrupt:
           GPIO.cleanup()

def start_warning_thread():
    """start this function as a subprocess

    Args:
        threshold_exceeded (bool): whether the actuator should be on or off
    """
    thread = threading.Thread(target=temp_threshold_warning)
    thread.daemon = True
    thread.start()
    

def update_threshold(state):
    """updates the thread

    Args:
        state (bool): whether the state should be updated or not
    """
    if state:
        threshold_exceeded.set()
    else: threshold_exceeded.clear()