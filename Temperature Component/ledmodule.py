import RPi.GPIO as GPIO # type: ignore
import time
import threading

#constants
LED_PIN = 23
LED_PINB = 16




GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(LED_PINB, GPIO.OUT)


def temp_threshold_warning(threshold_exceeded):
    """triggers actuator in response to edge module data analysis

    Args:
        threshold_exceeded (bool): whether the actuator should be on or off
    """
    
    try:
        if(threshold_exceeded):
            while threshold_exceeded:
                #Turn warning LED ON
                GPIO.output(LED_PIN, GPIO.HIGH)
                time.sleep(3)
                
                GPIO.output(LED_PIN, GPIO.LOW)
                time.sleep(3)
        else:
            #turn green LED on
            GPIO.output(LED_PINB, GPIO.HIGH)
    except KeyboardInterrupt:
           GPIO.cleanup()

def start_warning_thread(threshold_exceeded):
    """start this function as a subprocess

    Args:
        threshold_exceeded (bool): whether the actuator should be on or off
    """
    thread = threading(target=temp_threshold_warning(threshold_exceeded))
    thread.daemon = True
    thread.start()