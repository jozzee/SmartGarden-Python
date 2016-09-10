import time
import RPi.GPIO as GPIO
import Sensors.WaterFlow as wf
import SharedPreferences as sp

statusSlat = "statusSlat"
delay = 5
delayWater = 10
minPulse = 0.115

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(29,GPIO.OUT)#facuet
GPIO.setup(31,GPIO.OUT)#shower
GPIO.setup(33,GPIO.OUT)#open slat
GPIO.setup(35,GPIO.OUT)#close slat
GPIO.setup(15,GPIO.IN)#input check status slat
GPIO.setup(40,GPIO.OUT)#output for test slat

def initSharedPreferences():
    sp.getSharedPreferences("Memoery")

initSharedPreferences()

def resetGPIO():
    print("Controls: reset GPIO")
    GPIO.output(29,False)
    GPIO.output(31,False)
    GPIO.output(33,False)
    GPIO.output(35,False)
    GPIO.output(40,False)
    
def water():
    print("  - Controls: water...")
    wf.setZero()
    GPIO.output(29,True)
    time.sleep(int(delayWater))
    print(str(wf.getFlow()))
    GPIO.output(29,False)
    if(wf.isWaterFlows()):#wf.getFlow()>float(minPulse)
        print("    - water on work" )  
        return True
    else:
        print("    - water falsed!!!" )
        return False

def shower():
    print("  - Controls: shower...")
    wf.setZero()
    GPIO.output(31,True)
    time.sleep(delay)
    GPIO.output(31,False)
    if(wf.isWaterFlows()):#wf.getFlow()>float(minPulse)
        print("    - water on work" )  
        return True
    else:
        print("    - water falsed!!!" )
        return False  #False

def closeSlat():
    print("  - Controls: closeSlat...")
    initSharedPreferences()
    print("slat status: "+str(sp.get(statusSlat)))
    if(int(sp.get(statusSlat)) == int(1)):
        GPIO.output(33,True)
        GPIO.output(35,False)
        time.sleep(1)
        GPIO.output(33,False)
        GPIO.output(35,False)
        return True
    else:
        print("  -  Slat is closed")
        return False
def openSlat():
    print("  - Controls: openSlat...")
    initSharedPreferences()
    if(int(sp.get(statusSlat)) == int(2)):
        GPIO.output(33,False)
        GPIO.output(35,True)
        time.sleep(1)
        GPIO.output(33,False)
        GPIO.output(35,False)
        return True
    else:
        print("  -  Slat is opened")
        return False


    
