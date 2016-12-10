#!/usr/bin/env python

import time
import json
import RPi.GPIO as GPIO
import Network as network
import MicroGear as gear
import Time as t
import Inputs as inputs
import preference.SharedPreferences as sp
import Database as db
import Compare as compare
import Controls as ctrl
import Clock as alarmClock
import GCM as gcm

mosStd = "mosStd"           #moisture standard
tmpStd = "tmpStd"           #temp standard
ligStd = "ligStd"           #light standard

fqPData = "fqPData"         #frequency to publish data to netpie
fqPImage = "fqPImage"       #frequency to publish image to netpie
fqIData = "fqIData"         #frequency to insert data to database
fqShower = "fqShower"       #frequency to shower (0 = auto, > 0 = user setting)
ageData = "ageData"         #day off store data in database
lastUpdate = "lastUpdate"   #last update  data
autoMode = "autoMode"       #auto mode
slatStatus = "slatStatus"   #status of slat

nextTimePubData = 0
nextTimePubImage = 0
nextTimeInsertData = 0
timeExceptWater = 0
timeExceptShower = 0
lastTimeShower = 0
lastTimePubImage = 0
stSlat = None



global isConn
global timeCheckNet
fqCheckNet = 600 # 600 is 10 mintue

sensorPoint = 2


def checkNet(timeStamp):
  global timeCheckNet
  if(int(timeStamp) >= int(timeCheckNet)):
    print("Main, check is connect internet in Main loop")
    if(network.isConnectInternet()):
      global isConn
      if(isConn == False):
        isConn = True
        gear.onConnection() #connect netpie
    else:
      global isConn
      isConn = False
    timeCheckNet = (int(time.time())+int(fqCheckNet))
  else:
    #print("next time to check net: "+str(t.timeStampToDateTime(timeCheckNet)))
    print("")
    
def getNetStatus():
  if(isConn):
    return "Connected to Internet"
  else:
    return "No Internet Connection"
  
def getSlatStatus(lightIn,lightOut):
  print(" get slat status")

  stSlat = int(sp.get(slatStatus))
  print("  slat status from preference: "+str(stSlat))
  if((float(lightIn) >0) and (float(lightOut) > 0)):
    #print("  light in: "+str(lightIn) +" lux")
    #print("  light out: "+str(lightOut) +" lux")
    if((float(lightOut)-float(lightIn))>float(3000)): #value have different motr than 2,000 lux
      if(stSlat != int(0)):
        print("  light in and out different more 3000 lux, But slat status = open (1)")
        if(ctrl.closeSlat()): #if can close slat
          time.sleep(10)
          sp.put(slatStatus,int(0))
          global isConn
          if(isConn):
            gear.publisSlatStatus(0)
        stSlat = 0
    else:
      if(int(stSlat) == 0):
        if((float(lightOut)-float(lightIn))<float(1000)):
          if(ctrl.openSlat()):
            time.sleep(10)
            sp.put(slatStatus,int(1))
            global isConn
            if(isConn):
              gear.publisSlatStatus(1)
        stSlat = 1
  else:
    print("  sensor light error!!")
  return stSlat
  

def MainFunction():
  inputs.setSensorPoint(sensorPoint)
  while True:
    print("")
    alarmClock.getAlarmList()
    have,body = alarmClock.haveAlarmClock()
    if(have and isConn):
      gear.onRefreshRawData()
      gear.publisLogDataList()
      gear.publisSlatStatus(sp.get(slatStatus))
      noti = gcm.setData("alarm",str(body))
      gcm.pushNotification(noti)
    else:
      print("not alarm clock")
        
    timeStamp = int(time.time())
    print(str(timeStamp) +" (" +str(t.timeStampToDateTime(timeStamp)) +") " +getNetStatus())

    if(gear.isHasReload()):
      reload()
      
    mosObj = json.loads(inputs.getMoistureObject())
    temObj = json.loads(inputs.getTempObject())
    ligObj = json.loads(inputs.getLightObject())

    if(sp.get(autoMode)):
      global stSlat
      stSlat = getSlatStatus(ligObj["light_in"],ligObj["light_out"])
    else:
      stSlat = sp.get("slatStatus")
    
    if(mosObj["average"] > 0):
      for i in range(0,int(sensorPoint)):
        print(" moisture at point " +str(i+1) +": " +str(mosObj[("point"+str(i+1))]) +" %")
    else:
      print(" moisture sensors error!")
    if(temObj["average"] > 0):
      for i in range(0,int(sensorPoint)):
        print(" temp at point     " +str(i+1) +":   " +str(temObj[("point"+str(i+1))]) +" *C")
    else:
      print(" temp sensors error!")
    print(" lightIn:          "+str(ligObj["light_in"]) +" Lux")
    print(" lightOut:         "+str(ligObj["light_out"]) +" Lux")
    print(" slat status:      "+str(stSlat))
    print("")

    print("  mosStd: "+str(sp.get(mosStd)))
    print("  tmpStd: "+str(sp.get(tmpStd)))
    print("  ligStd: "+str(sp.get(ligStd)))
    print("  fqPData: "+str(sp.get(fqPData)))
    print("  fqPImage: "+str(sp.get(fqPImage)))
    print("  fqIData: "+str(sp.get(fqIData)))
    print("  fqShower: "+str(sp.get(fqShower)))
    print("  ageData: "+str(sp.get(ageData)))
    print("  lastUpdate: "+str(sp.get(lastUpdate)))
    print("  autoMode: "+str(sp.get(autoMode)))
    print("")

    global isConn
    global nextTimePubData
    global nextTimePubImage
    global nextTimeInsertData
    global lastTimePubImage
    
    if(int(timeStamp) >= int(nextTimePubData)):
      if(isConn):
        payload = "{\"time\":"+str(timeStamp)+",\"moisture\":"+str(json.dumps(mosObj))+",\"temp\":"+str(json.dumps(temObj)+",\"light\":"+str(json.dumps(ligObj)))+"}"
        result, nextTime = gear.publishRawData(str(payload),sp.get(fqPData),timeStamp)
        if(result):
          nextTimePubData = nextTime
    if(int(timeStamp) >= int(nextTimePubImage)):
      if(isConn):
        result, nextTime = gear.publishImage(sp.get(fqPImage),timeStamp)
        if(result):
          nextTimePubImage = nextTime
          lastTimePubImage = timeStamp
    if(int(timeStamp) >= int(nextTimeInsertData)):
      reult, nextTime = db.insertRawData(timeStamp,mosObj,temObj,ligObj)
      if(reult):
        nextTimeInsertData = nextTime
        if(isConn):
          gear.publisRawDataList()

    print("")
    print(" nextTimePubData: "+str(t.timeStampToDateTime(nextTimePubData)))
    print(" nextTimePubImage: "+str(t.timeStampToDateTime(nextTimePubImage)))
    print(" nextTimeInsertData: "+str(t.timeStampToDateTime(nextTimeInsertData)))
    print("")

    #Compare and validate
    global timeExceptWater
    global timeExceptShower
    
    if(sp.get(autoMode)):
       print("\nOn Work in Auto Mode...")
       if(t.isDay()):
         #-----------------------------------------------
         
         if(int(timeStamp)>int(timeExceptWater)):
           result,timeExcept = compare.compareMosture(timeStamp,mosObj,isConn)
           if(result):
             if(isConn):
               gear.publisLogDataList()
             timeExceptWater = 0
           else:
             if(int(timeExcept)>0):
               timeExceptWater = timeExcept
         else:
           print("wait to "+str(t.timeStampToDateTime(timeExceptWater)) +" for water agains ")

         #-----------------------------------------------
           
         global lastTimeShower
         if(int(timeStamp)>int(timeExceptShower)):
           result,timeExcept = compare.compareTemp(timeStamp,temObj,lastTimeShower,isConn,mosObj,stSlat,ligObj)
           if(result):
             if(isConn):
               gear.publisLogDataList()
             timeExceptShower = 0
             lastTimeShower = timeStamp
             sp.put("lastTimeShower",lastTimeShower)
           else:
             if(int(timeExcept)>0):
               timeExceptShower = timeExcept
         else:
           print("wait to "+str(t.timeStampToDateTime(timeExceptShower)) +" for shower agains")

         #------------------------------------------------

         result, st = compare.compareLight(timeStamp,ligObj,stSlat,isConn)
         if(result):
           if(isConn):
             gear.publisSlatStatus(st)

         #-------------------------------------------------
            
       else:
         print(" But this time is a nigth!...")
    else:
      print("manual mode....")
     
    checkNet(timeStamp)
    print("----------------------------------------------------\n")
    
    time.sleep(10)
    

def testFunction():
  while True:
    gear.publis("test",str(int(time.time())))
    time.sleep(2)
def reload():
  global nextTimePubData
  global nextTimeInsertData
  global nextTimePubImage
  global lastTimePubImage
  nextTimePubImage = int(int(lastTimePubImage)+(int(sp.get(fqPImage))*int(3600))) #1 hour in time stamp
  nextTimePubData = t.getNextTimePubData(sp.get(fqPData))
  nextTimeInsertData = t.getNextTimeInsertData(sp.get(fqIData))
  
#Start!!!-------------------------------------------
sp.getSharedPreferences()
global nextTimePubData
global nextTimeInsertData
nextTimePubData = t.getNextTimePubData(sp.get(fqPData))
nextTimeInsertData = t.getNextTimeInsertData(sp.get(fqIData))


if(network.isConnectInternet()):
  print("is connect internet")
  global isConn
  global timeCheckNet
  isConn = True
  timeCheckNet = (int(time.time())+int(fqCheckNet))
  gear.onConnection() #connect netpie
  ligObj = json.loads(inputs.getLightObject())
  gear.publisSlatStatus(getSlatStatus(ligObj["light_in"],ligObj["light_out"]))
  MainFunction()
else:
  print("no internet connection")
  global isConn
  global timeCheckNet
  isConn = False
  timeCheckNet = (int(time.time())+int(fqCheckNet))
  MainFunction()
