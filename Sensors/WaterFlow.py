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
    global flow
    flow = (count * 2.69541779) / 1000
    print("WaterFlows, flows: "+str(flow))
    
def setZero():
    print("  WaterFlows, setZero")
    global count
    count = 0
    global flow
    flow = 0
    
def getFlow():
    global flow
    print("  WaterFlows, getFlow: "+str(flow))
    return flow

def isWaterFlows():
    if(flow>standardPulse):
        return True
    else:
        return False

GPIO.add_event_detect(FLOW_SENSOR, GPIO.FALLING, callback=countPulse)#FALLING
print("WaterFlows, add event from water flows sensor")

    
