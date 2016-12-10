import sensors.MCP3008 as mcp3008
import sensors.DHT22 as dht22
import sensors.BH1750 as bh1750
import pigpio
import base64
import picamera
import os
import time

sensorPoint = 2

pi = pigpio.pi() #Initiate GPIO for pigpio
#Setup the sensor dht22
dht22_1 = dht22.sensor(pi,4)# (7) #use the actual GPIO pin name
dht22_2 = dht22.sensor(pi,17)#(11) #use the actual GPIO pin name
dht22_1.trigger()
dht22_2.trigger()

def subDecimal(val):
    sub =  val.split(".")
    if(len(sub)==2):
        sub[1] = (sub[1])[:2]
        return(sub[0]+"."+sub[1])
    else:
        return val

def setSensorPoint(point):
    if((int(point)>0)and(int(point) <= 4)):
        global sensorPoint
        sensorPoint = point
    else:
        print("Exception!! point has 1-4")
def getMoisture(address):
    if((int(address)>= 0) and (int(address)<= 7)):
        return mcp3008.readMoisture(address)
    else:
        print("Exception!! address has 0-7")
        return -1
def getMoistureObject():
    erPoint = 0;
    valSum = -1
    result = "{"
    for i in range(0,int(sensorPoint)):
        val = getMoisture(i)
        if(val<0):
            erPoint+=1;
        else:
            if(valSum == (-1)):
                valSum = 0
            valSum += val
        result += "\"point" +str((i+1)) +"\":" +str(val)
        if(int(i+1)<int(sensorPoint)):
            result +=","
    if(int(sensorPoint)>1):
        div = (int(sensorPoint)-int(erPoint))
        if(div>0):
            av  = float(float(valSum)/int(div))
            result +=(",\"average\":"+subDecimal(str(av)))
        else:
            result +=(",\"average\":"+str(valSum))
    else:
        result +=(",\"average\":"+str(valSum))
    result += "}"
    #print(result)
    return result
    
def getTemp(point):
    if(int(point) == 1):
        #print("get temp as point 1")
        dht22_1.trigger()
        #time.sleep(.12)
        temp = ('%.2f' % (dht22_1.temperature()))
        if(temp == "-999.00"):
            temp = -1
        return temp
    elif(int(point) == 2):
        #print("get temp as point 2")
        dht22_2.trigger()
        #time.sleep(.12)
        temp = ('%.2f' % (dht22_2.temperature()))
        if(temp == "-999.00"):
            temp = -1
        return temp

def getTempObject():
    erPoint = 0;
    valSum = -1
    result = "{"
    for i in range(0,int(sensorPoint)):
        val = getTemp((i+1))
        if(float(val)<0):
            erPoint+=1;
        else:
            if(valSum == (-1)):
                valSum = 0
            valSum += float(val)
        result += "\"point" +str((i+1)) +"\":" +str(val)
        if(int(i+1)<int(sensorPoint)):
            result +=","
    if(int(sensorPoint)>1):
        div = (int(sensorPoint)-int(erPoint))
        if(int(div)>0):   
            av  = float(float(valSum)/(int(sensorPoint)-int(erPoint)))
            result +=(",\"average\":"+str(av))
        else:
            result +=(",\"average\":"+str(valSum))
    else:
        result +=(",\"average\":"+str(valSum))
    result += "}"
    #print(result)
    return str(result)

def getHumidity(): #ezxample how to get air humity from dht22
    dht22_1.trigger()
    h = ('%.2f' % (dht22_1.humidity()))
    if(h == "-999.00"):
        h = -1 
    return h
    

def getLight(address):
    if(int(address) == 1):
        return bh1750.readLight(0x23)
    elif(int(address) == 2):
        return bh1750.readLight(0x5C)
    else:
        print("Exception!! address has 1-2")
        return -1
    
def getLightObject():
    l1 = bh1750.readLight(0x23) 
    l2 = bh1750.readLight(0x5C)
    result = "{\"light_in\":"+str(l1) +",\"light_out\":"+str(l2)+"}"
    #print(result)
    return str(result)
    
def captureImage():
    os.system("fswebcam -r 1280x720 --no-banner image/garden.jpg")
    print("Inputs, captureImage success")
    
def cvIM2Base64():#cv: convernt
    with open("image/garden.jpg","rb") as imageFile:
        imageAsString = base64.b64encode(imageFile.read())
    return imageAsString.decode('utf-8')

