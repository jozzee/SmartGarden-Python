import RPi.GPIO as GPIO
import time
GPIO.output(29,True)
time.sleep(10)
GPIO.output(29,False)
