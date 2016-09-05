import Sensors.MCP3008 as mcp3008
import Sensors.DHT22 as dht22
import Sensors.BH1750 as bh1750
import pigpio
import base64
import picamera
import os
import time


#Initiate GPIO for pigpio
pi = pigpio.pi()
#Setup the sensor
dht_1 = dht22.sensor(pi,4)#(4,17) #use the actual GPIO pin name
dht_2 = dht22.sensor(pi,17)#(4,17) #use the actual GPIO pin name
dht_1.trigger()
dht_2.trigger()
#Status sensor for use ShaeMem json ---------
stDHT_1 = True
stDHT_2 = True


def getMoisture(address):
    if((int(address)>= 0) and (int(address)<= 7)):
        return mcp3008.readMoisture(address)
    else:
        print("Exception!! address has 0-7")
        return -1
    
def getMoistureSet():
    m1 = getMoisture(0)
    m2 = getMoisture(1)
    mAverage = -1
    if((float(m1) > 0) and (float(m1) > 0)):
        mAverage = float(((float(m1)+float(m2))/2))
    elif((float(m1) < 0) and (float(m2) > 0)):
        mAverage = float(m2)
    elif((float(m1) > 0) and (float(m2) < 0)):
        mAverage = float(m1)
    return m1,m2,mAverage

def getTemp(address):
    if(int(address) == 1):
        dht_1.trigger()
        temp = ('%.2f' % (dht_1.temperature()))
        if(temp == "-999.00"):
            temp = -1 
        return temp
    elif(int(address) == 2):
        dht_2.trigger()
        temp = ('%.2f' % (dht_2.temperature()))
        if(temp == "-999.00"):
            temp = -1 
        return temp
    else:
        print("Exception!! address has 1-2")
        return -1
    
def getHumidity(address):
    if(int(address) == 1):
        dht_1.trigger()
        h = ('%.2f' % (dht_1.humidity()))
        if(h == "-999.00"):
            h = -1 
        return h
    elif(int(address) == 2):
        dht_2.trigger()
        h = ('%.2f' % (dht_2.temperature()))
        if(h == "-999.00"):
            h = -1 
        return h
    
def getTempSet():
    t1 = getTemp(1)
    t2 = getTemp(2)
    tAverage = -1
    if((float(t1) > 0) and (float(t2) > 0)):
        tAverage = float(((float(t1)+float(t2))/2))
    elif((float(t1) < 0) and (float(t2) > 0)):
        tAverage = float(t2)
    elif((float(t1) > 0) and (float(t2) < 0)):
        tAverage = float(t1)
    return t1,t2,tAverage

def getLight(address):
    if(int(address) == 1):
        return bh1750.readLight(0x23)
    elif(int(address) == 2):
        return bh1750.readLight(0x5C)
    else:
        print("Exception!! address has 1-2")
        return -1
    
def getLightSet():
    l1 = getLight(1)
    l2 = getLight(2)
    lAverage = -1
    if((float(l1) > 0) and (float(l2) > 0)):
        lAverage = float(((float(l1)+float(l2))/2))
    elif((float(l1) < 0) and (float(l2) > 0)):
        lAverage = float(l2)
    elif((float(l1) > 0) and (float(l2) < 0)):
        lAverage = float(l1)
    return l1,l2,lAverage

def captureImage():
    os.system("fswebcam -r 1280x720 --no-banner /home/pi/Desktop/SmartGarden_v7/Image/garden.jpg")
    
def cvIM2Base64():#cv: convernt
    with open("/home/pi/Desktop/SmartGarden_v7/Image/garden.jpg","rb") as imageFile:
        imageAsString = base64.b64encode(imageFile.read())
    return imageAsString.decode('utf-8')

    


