import time
import RPi.GPIO as GPIO

GPIO.output(33,True)
GPIO.output(35,False)
time.sleep(1)
GPIO.output(33,False)
GPIO.output(35,False)
