#!/usr/bin/env python

import microgear.client as microgear
import json
import time
import Inputs as inputs
import preference.SharedPreferences as sp
import Database as db
import Time as t
import Controls as ctrl
import Clock as alarmClock

minuteStamp =  60 # 1 mintue in time stamp
hourStamp = 3600 # 1 hour in time stamp
con = False

appId = "<App Id>"
appKey = "<Gear Key>"
appSecret =  "<Gear Secret>"
hasReload = False

microgear.create(appKey,appSecret,appId,{'debugmode': True})
sp.getSharedPreferences()

def isHasReload():
    global hasReload
    if(hasReload):
        hasReload = False
        return True
    
def isConnect():
    global con
    return con

def publis(topic,payload):
    if(isConnect()):
        print("Microgear, publish topic: "+str(topic)+" to netpie")
        microgear.publish(str("/"+topic),str(payload))
    else:
        print("Microgear, Exception!! microgear not connect")
        
def publishImage(fq,timeStamp): #frequency in hour unit
    
    if(isConnect()):
        print("Microgear, publish Image to netpie")
        inputs.captureImage()
        microgear.publish("/photo",str(timeStamp)+","+str(inputs.cvIM2Base64()),{'retain':True})
        microgear.publish("/hasPhoto","1") #publish to app for load image
        return True,int(int(timeStamp)+(int(fq)*int(hourStamp))) #retuen result and next time to publis image
    else:
        print("Microgear, Exception!! microgear not connect")
        return False,0 #return false
    
def refreshImage():
    if(isConnect()):
        print("Microgear, publish Image to netpie")
        inputs.captureImage()
        microgear.publish("/photo",str(timeStamp)+","+str(inputs.cvIM2Base64()),{'retain':True})
        microgear.publish("/hasPhoto","1") #publish to app for load image
        response = json.dumps({"topic":"refreshIM","success":True,"message":payload})
        microgear.publish("/response",str(response))
        
def publishRawData(payload,fq,timeStamp):
    if(isConnect()):
        print("Microgear, publish Data to netpie")
        microgear.publish("/rawData",str(payload),{'retain':True})
        return True,int(int(timeStamp)+(int(fq)*int(minuteStamp))) #return result and next time to publish data
    else:
        print("Microgear, Exception!! microgear not connect")
        return False,0 #return false
    
def publisRawDataList():
    if(isConnect()):
        print("Microgear, publish Data List to netpie")
        result, data = db.selectRawDataList()
        if(result):
            microgear.publish("/rawDataList",str(data),{'retain':True})
            microgear.publish("/hasRawList","1")
    else:
        print("Microgear, Exception!! microgear not connect")
        
def publisLogDataList():
    if(isConnect()):
        print("Microgear, publish History List to netpie")
        result, data = db.selectLogDataList()
        if(result):
            microgear.publish("/logDataList",str(data),{'retain':True})
            microgear.publish("/hasLogList","1")
    else:
        print("Microgear, Exception!! microgear not connect")
        
def publisSlatStatus(slatStatus): # 0 is close, 1 is open
    if(isConnect()):
        microgear.publish("/slatStatus",str(slatStatus),{'retain':True})
        print("Microgear, publish Slat Status ("+str(slatStatus) +") to netpie")
    else:
        print("Microgear, Exception!! microgear not connect")

def settingDetails(payload):
    fqPData = "fqPData"         #frequency to publish data to netpie
    fqPImage = "fqPImage"       #frequency to publish image to netpie
    fqIData = "fqIData"         #frequency to insert data to database
    fqShower = "fqShower"       #frequency to shower (0 = auto, > 0 = user setting)
    ageData = "ageData"         #day off store data in database
    autoMode = "autoMode"       #auto mode
    lastUpdate = "lastUpdate"

    objDetails = json.loads(payload)

    if(int(objDetails[lastUpdate]) > int(sp.get(lastUpdate))):

        global hasReload
        hasReload = True

        for i in objDetails:
            print("  - key: "+str(i))
            print("  - value: "+str(objDetails[i]))
            print("  ---------------------")
            
            if(i == fqPData ):
                sp.put(fqPData,objDetails[i])
                
            elif(i== fqPImage):
                sp.put(fqPImage,objDetails[i])
                
            elif(i== fqIData):
                sp.put( fqIData,objDetails[i])
                
            elif(i == fqShower):
                sp.put(fqShower,objDetails[i])
               
            elif(i == ageData):
                sp.put(ageData,objDetails[i])
      
            elif(i== autoMode):
                sp.put(autoMode,objDetails[i])
            elif(i == lastUpdate):
                sp.put(lastUpdate,objDetails[i])
                
        if(isConnect()):
            response = json.dumps({"topic":"settingDetails","success":True,"message":payload})
            microgear.publish("/response",str(response))

def settingStandard(payload):

    mosStd = "mosStd"           #moisture standard
    tmpStd = "tmpStd"           #temp standard
    ligStd = "ligStd"           #light standard

    #errorCode  0: database error
    #           1: water not flows
    #           2: water not true arare
    #           3: temp not decrease after shower
    #           4: not time to shower
    #           5: slat is opened
    #           6: slat is closed
    #           7: light value not decrease
    
    objecStan = json.loads(payload)
    for i in objecStan:
        print("  - key: "+str(i))
        print("  - value: "+str(objecStan[i]))
        print("  ---------------------")
        if(i == mosStd):
            sp.put(mosStd,objecStan[i])
        elif(i == tmpStd):
            sp.put(tmpStd,objecStan[i])
        elif(i == ligStd):
            sp.put(ligStd,objecStan[i]) 
    if(isConnect()):
        response = json.dumps({"topic":"settingStandard","success":True,"message":payload})
        microgear.publish("/response",str(response))

def onRefreshRawData():
    mosObj = json.loads(inputs.getMoistureObject())
    temObj = json.loads(inputs.getTempObject())
    ligObj = json.loads(inputs.getLightObject())
    timeStamp = int(time.time())
    
    payload = "{\"time\":"+str(timeStamp)+",\"moisture\":"+str(json.dumps(mosObj))+",\"temp\":"+str(json.dumps(temObj)+",\"light\":"+str(json.dumps(ligObj)))+"}"
    microgear.publish("/rawData",str(payload),{'retain':True})

def controlsDevices(payload):
    success = False
    message = ""
    response = None
    
    if(payload == 1):
        print(" Water from user command")
        mosObj = json.loads(inputs.getMoistureObject())
        if(ctrl.water()): 
            time.sleep(10) #wait 10 second
            newMosObj = json.loads(inputs.getMoistureObject())
            print("  old moisture: "+str(mosObj["average"]))
            print("  new moisture: "+str(newMosObj["average"]))
            if((float(newMosObj["average"]-float(mosObj["average"])>5))):# if moisture value more than valus before
                onRefreshRawData()
                result = db.insertLogData(int(time.time()),1,2,float(mosObj["average"]),float(newMosObj["average"])) #insert log to database
                if(result):
                    print("  All success")
                    success = True
                    message = json.dumps({"working":payload,"valBefore":float(mosObj["average"]),"valAfter":float(newMosObj["average"])})
                    publisLogDataList()
                else:
                    message = json.dumps({"errorCode":0,"msg":"database error","working":payload,"valBefore":float(mosObj["average"]),"valAfter":float(newMosObj["average"])})  
            else:
                if((float(newMosObj["average"])>float(mosObj["average"]))>=1):
                    message = json.dumps({"errorCode":8,"working":payload,"valBefore":float(mosObj["average"]),"valAfter":float(newMosObj["average"])})
                    publisLogDataList()
                else:   
                    print("  Error! water not true Arare")
                    message = json.dumps({"working":payload,"errorCode":2,"msg":"water not true arare"})
        else:
            print("  Error! water not flows")
            message = json.dumps({"working":payload,"errorCode":1,"msg":"water not flows"})
     
    elif(payload == 2):
        print(" Shower from user command")
        fqShower = "fqShower"       #frequency to shower (0 = auto, > 0 = user setting)
        timeStamp = int(time.time())
        lastTimeShower = sp.get("lastTimeShower")
        print("lastTimeShower: "+str(lastTimeShower))
        minStamp = 60
        m = ""
        fq = sp.get(fqShower)
        if(fq == 0):
            fq = t.getFqShower()#get ferquency from system (fq in minute *60) minStamp
        if(int(timeStamp)>=(int(lastTimeShower)+(int(fq)*int(minStamp)))):
            temObj = json.loads(inputs.getTempObject())
            if(ctrl.shower()):
                time.sleep(10)
                newTemObj = json.loads(inputs.getTempObject())
                print("  old temp: "+str(temObj["average"]))
                print("  new temp: "+str(newTemObj["average"]))
                if(float(newTemObj["average"])<=float(temObj["average"])):
                    onRefreshRawData()
                    result = db.insertLogData(timeStamp,2,2,float(temObj["average"]),float(newTemObj["average"])) #insert log to database
                    if(result):
                        success = True
                        message = json.dumps({"working":payload,"valBefore":float(temObj["average"]),"valAfter":float(newTemObj["average"])})
                        print("  All success")
                        publisLogDataList()
                        sp.put("lastTimeShower",timeStamp)
                    else:
                        message = json.dumps({"errorCode":0,"msg":"database error","working":payload,"valBefore":float(temObj["average"]),"valAfter":float(newTemObj["average"])})
                else:
                    print(" Error! temp not decrease after shower")
                    message = json.dumps({"working":payload,"errorCode":3,"msg":"temp not decrease after shower"})
            else:
                print(" Error! water not flows")
                message = json.dumps({"working":payload,"errorCode":1,"msg":"water not flows"})
        else:
            nextTime = (int(lastTimeShower)+(int(fq)*int(minStamp)))
            print(" not time to shower, Working again at "+str(t.timeStampToDateTime(nextTime)))
            message = json.dumps({"working":payload,"errorCode":4,"msg":str(nextTime)})
 
    elif(payload == 3):
        print(" Open slat from user command")
        slatStatus = sp.get("slatStatus")   #status of slat
        print("  slatStatus: " +str(slatStatus))
        if(int(slatStatus) != 1):
            ligObj = json.loads(inputs.getLightObject())
            if(ctrl.openSlat()):#if can open slat
                time.sleep(10)
                newLigObj = json.loads(inputs.getLightObject())
                sp.put("slatStatus",str("1"))
                publisSlatStatus(1)
                result = db.insertLogData(int(time.time()),3,2,float(ligObj["light_in"]),float(newLigObj["light_in"])) #insert log to database
                onRefreshRawData()
                if(result):
                    publisLogDataList()
                    success = True
                    message = json.dumps({"working":payload,"valBefore":float(ligObj["light_in"]),"valAfter":float(newLigObj["light_in"])})
                    print("  All success")
                else:
                    message = json.dumps({"errorCode":0,"msg":"database error","working":payload,"valBefore":float(ligObj["light_in"]),"valAfter":float(newLigObj["light_in"])})
                    
        else:
            print("  slat is opened (1)")
            message = json.dumps({"working":payload,"errorCode":5,"msg":"slat is opened"})

    elif(payload == 4):
        print(" Close slat from user command")
        slatStatus = sp.get("slatStatus")   #status of slat
        print("  slatStatus: " +str(slatStatus))
        if(int(slatStatus) != 0):
            ligObj = json.loads(inputs.getLightObject())
            if(ctrl.closeSlat()): #if can close slat
                time.sleep(10)
                newLigObj = json.loads(inputs.getLightObject())
                print("  old light: "+str(ligObj["light_in"]))
                print("  new light: "+str(newLigObj["light_in"]))
                
                sp.put("slatStatus",str("0"))
                publisSlatStatus(0)
                result = db.insertLogData(int(time.time()),4,2,float(ligObj["light_in"]),float(newLigObj["light_in"])) #insert log to database
                onRefreshRawData()
                if(result):
                    publisLogDataList()
                else:
                    message = json.dumps({"errorCode":0,"msg":"database error","working":payload,"valBefore":float(ligObj["light_in"]),"valAfter":float(newLigObj["light_in"])})
                    
                if(float(newLigObj["light_in"]) < float(ligObj["light_in"])):
                    success = True
                    message = json.dumps({"working":payload,"valBefore":float(ligObj["light_in"]),"valAfter":float(newLigObj["light_in"])})
                else:
                    print("  new light value not decrease")
                    message = json.dumps({"working":payload,"errorCode":7,"msg":"light value not decrease"})
        else:
            print("  slat is closed (0)")
            message = json.dumps({"working":payload,"errorCode":6,"msg":"slat is closed"})

    response = json.dumps({"topic":"controlDevices","success":success,"message":message})
    #print("response: "+str(response))
    if(isConnect()):
        microgear.publish("/response",str(response))

def onRefresh():
    mosObj = json.loads(inputs.getMoistureObject())
    temObj = json.loads(inputs.getTempObject())
    ligObj = json.loads(inputs.getLightObject())
    timeStamp = int(time.time())
    
    payload = "{\"time\":"+str(timeStamp)+",\"moisture\":"+str(json.dumps(mosObj))+",\"temp\":"+str(json.dumps(temObj)+",\"light\":"+str(json.dumps(ligObj)))+"}"
    microgear.publish("/rawData",str(payload),{'retain':True})

    response = json.dumps({"topic":"refresh","success":True,"message":""})
    microgear.publish("/response",str(response))
    
    inputs.captureImage()
    microgear.publish("/photo",str(timeStamp)+","+str(inputs.cvIM2Base64()),{'retain':True})
    microgear.publish("/hasPhoto","1") #publish to app for load image

def onSaveClock(payload):
    alarmSet = json.loads(payload)
    alarmClock.setAlarmToText(alarmSet)
    response = json.dumps({"topic":"alarm","success":True,"message":payload})
    microgear.publish("/response",str(response))
        
#Micro gear function
#---------------------------------------------------------------------------------
def connection():
    global con
    con = True
    print ("Microgear, Now I am connected with netpie")
  
def disconnect():
    global con
    con = False
    print ("Microgear, Disconnect is work")
  
def subscription(topic,message):
    topic = topic.split("/")
    topic = topic[2]
    payload = message[2:-1]
    print ("\nMicrogear, on subscription \n topic: "+topic+"\n message: "+message +"\n")
    #print ("-----------------------")

    if(topic == "preferences"):
        sp.setSharedPreferences(json.loads(payload))
    elif(topic == "token"):
        sp.put("token",payload)
    elif(topic == "slatStatus"):
        sp.put("slatStatus",payload)
    elif(topic == "refreshIM"):
        refreshImage()
    elif(topic == "settingDetails"):
        settingDetails(payload)
    elif(topic == "settingStandard"):
        settingStandard(payload)
    elif(topic == "controlDevices"):
        controlsDevices(int(payload))
    elif(topic == "refresh"):
        onRefresh()
    elif(topic == "alarm"):
        onSaveClock(payload)
        
        
def present(gearkey):
    gearkey = gearkey[2:-1]
    obj = json.loads(gearkey)
    print("Microgear, gear name: " +obj["alias"] +" become online")

def absent(gearkey):
    gearkey = gearkey[2:-1]
    obj = json.loads(gearkey)
    print("Microgear, gear name: " +obj["alias"] +" offline!...")

def warning(msg):
    print("Microgear, warning: " +msg)
    
def info(msg):
    print("Microgear, info: " +msg)
    
def error(msg):
    print("Microgear, error: " +msg)

def onConnection():
    microgear.setalias("Raaspbery Pi - Python")
    microgear.on_connect = connection
    microgear.on_disconnect = disconnect
    microgear.on_message = subscription
    microgear.on_present = present
    microgear.on_absent = absent
    microgear.on_warning = warning
    microgear.on_info = info
    microgear.on_error = error
    microgear.subscribe("/token")
    microgear.subscribe("/refresh")
    microgear.subscribe("/settingStandard")
    microgear.subscribe("/settingDetails")
    microgear.subscribe("/controlDevices")
    microgear.subscribe("/alarm")
    microgear.connect()


