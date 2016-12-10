import time
import RPi.GPIO as GPIO
import sensors.WaterFlow as wf

statusSlat = "slatStatus"

delayWater = 10 
delayShower = 5
minPulse = 0.115

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(29,GPIO.OUT)#facuet
GPIO.setup(31,GPIO.OUT)#shower
GPIO.setup(33,GPIO.OUT)#open slat
GPIO.setup(35,GPIO.OUT)#close slat
GPIO.setup(15,GPIO.IN)#input check status slat
GPIO.setup(40,GPIO.OUT)#output for test slat


def resetGPIO():
    print("Controls, reset GPIO")
    GPIO.output(29,False)
    GPIO.output(31,False)
    GPIO.output(33,False)
    GPIO.output(35,False)
    GPIO.output(40,False)
    
def water():
    print(" Controls, water...")
    wf.setZero()
    GPIO.output(29,True)
    time.sleep(int(delayWater))
    #print(str(wf.getFlow()))
    GPIO.output(29,False)
    if(wf.isWaterFlows()):#wf.getFlow()>float(minPulse)
        print("  water flow" )  
        return True
    else:
        print("  water error!!" )
        return False

def shower():
    print("Controls, shower...")
    wf.setZero()
    GPIO.output(31,True)
    time.sleep(int(delayShower))
    GPIO.output(31,False)
    if(wf.isWaterFlows()):#wf.getFlow()>float(minPulse)
        print(" water flow" )  
        return True
    else:
        print(" water error!!" )
        return False  #False

#slat status 0 is close and 1 is open
def closeSlat():
    print(" Controls, closeSlat...")
    GPIO.output(33,True)
    GPIO.output(35,False)
    time.sleep(1)
    GPIO.output(33,False)
    GPIO.output(35,False)
    print("  slat is close success")
    return True

def openSlat():
    print(" Controls, openSlat...")
    GPIO.output(33,False)
    GPIO.output(35,True)
    time.sleep(1)
    GPIO.output(33,False)
    GPIO.output(35,False)
    print("  slat is open success")
    return True


    
