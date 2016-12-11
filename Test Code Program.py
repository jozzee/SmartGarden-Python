import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
FLOW_SENSOR = 37
global count
count = 0
GPIO.setup(FLOW_SENSOR, GPIO.IN, pull_up_down = GPIO.PUD_UP)
def countPulse(channel):
    global count
    count = count+1
GPIO.add_event_detect(FLOW_SENSOR, GPIO.FALLING, callback=countPulse)
