#!/usr/bin/python
import time, sys
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

FLOW_SENSOR = 37
GPIO.setup(FLOW_SENSOR, GPIO.IN, pull_up_down = GPIO.PUD_UP)#PUD_UP

standardPulse = float(0.115)
global count
count = 0
global flow
flow = 0
def countPulse(channel):
    global count
    count = count+1
    #print("Water Flow: countPulse "+str(count))
    #print (count)
    global flow
    flow = (count * 2.69541779) / 1000
    #print(str(flow))
def setZero():
    print("WaterFlows: setZero")
    global count
    count = 0
    global flow
    flow = 0
def getFlow():
    print("WaterFlows: getFlow")
    global flow
    return flow
def isWaterFlows():
    if(flow>standardPulse):
        return True
    else:
        return False

GPIO.add_event_detect(FLOW_SENSOR, GPIO.FALLING, callback=countPulse)#FALLING
print("add event")

    
