import time
import json
import RPi.GPIO as GPIO
import microgear.client as microgear
import SharedPreferences as sp
import Controls as ctrl
import Database as db
import Inputs as inputs

import Time as tm

gearkey = "23oRa3PnK8Czx91"                 #key
gearsecret =  "U1zuonSDIeEeokxAskiJJJTEW"   #secreet
appid = "ECPSmartGarden"                    #appID
fqPubRawData = "fqPubRawData"
fqPubImage = "fqPubImage"
fqInsertRawData = "fqInsertRawData"
lsPubRawData = "lsPubRawData"
lsPubImage = "lsPubImage"
lsInsertRawData = "lsInsertRawData"
lsShower = "lsShower"
dayStorage = "dayStorage"
autoMode = "autoMode"
statusSlat = "statusSlat"
moisture = "moisture"
temp = "temp"
light = "light"
waitTime1 = "waitTime1"
waitTime2 = "waitTime2"
timeExcept1 = "timeExcept1"
timeExcept2 = "timeExcept2"
countExcept1 = "countExcept1"
countExcept2 = "countExcept2"
token = "token"

global oneMintue
oneMintue = 60
global oneMour
oneMour = 3600
oldTemp = 0
oldLight = 0
excepMaxVal = 5
minAsTimeStamp = 60

    
GPIO.setwarnings(False) #to disable warnings.
GPIO.setmode(GPIO.BOARD)
initSharedPreferences()
ctrl.resetGPIO()

#------------Microgear Netpie-----------------------
microgear.create(gearkey,gearsecret,appid,{'debugmode': True})
def callback_connect() :
    print ("Main: Now I am connected with netpie....")
def callback_disconnect() :
    print ("Main: Disconnected")
def callback_message(msg) :
    topic = msg.topic
    topic = topic[1:]
    topic = topic.split("/")[1]
    payload = msg.payload.decode('utf-8')
    print ("Main: I got message from topic:  " +topic)

    if(topic == "token"):
        sp.put(token,payload)
        initSharedPreferences()
    
    elif(topic == "refreshIM"):
        pubIM()
        response = json.dumps({"topic":"refreshIM","success":True,"message":payload})
        microgear.publish("/response",str(response))
        
    elif(topic == "settingDetails"):
        objDetails = json.loads(payload)
        for i in objDetails:
            print("  - key: "+str(i))
            print("  - value: "+str(objDetails[i]))
            print("  ---------------------")
            if(i==fqPubRawData):
                sp.put(fqPubRawData,objDetails[i])
            elif(i==fqPubImage):
                sp.put(fqPubImage,objDetails[i])
            elif(i==fqInsertRawData):
                sp.put(fqInsertRawData,objDetails[i])
            elif(i==dayStorage):
                sp.put(dayStorage,objDetails[i])
            elif(i==autoMode):
                sp.put(autoMode,objDetails[i])
        initSharedPreferences()
        ct.initSharedPreferences()
        db.initSharedPreferences()
        tm.initSharedPreferences()
        response = json.dumps({"topic":"settingDetails","success":True,"message":payload})
        microgear.publish("/response",str(response))

    elif(topic == "settingStandard"):
        objecStan = json.loads(payload)
        if(objecStan['sensor'] == "SoilMoisture"):
            sp.put("moisture",objecStan['value'])
        elif(objecStan['sensor'] == "dht22"):
            sp.put("temp",objecStan['value'])
        elif(objecStan['sensor'] == "bh1750"):
           sp.put("light",objecStan['value']) 
        initSharedPreferences()
        ct.initSharedPreferences()
        db.initSharedPreferences()
        tm.initSharedPreferences()
        response = json.dumps({"topic":"settingStandard","success":True,"message":payload})
        microgear.publish("/response",str(response))

    elif(topic == "controlDevice"):
        obj = json.loads(payload)
        for i in obj:
            print("  - key: "+str(i))
            print("  - value: "+str(obj[i]))
            print("  ---------------------")
            if(i == "1"):
                result = False
                message = ""
                mB1,mB2,mBAverage = inputs.getMoistureSet()
                if(ct.facuet()):
                    print("water success")
                    mA1,mA2,mAAverage = inputs.getMoistureSet()
                    if(float(mAAverage)>float(mBAverage)):# if moisture value more than valus before
                        print("All success")
                        result = True
                        message = str(json.dumps({"mBAverage":mBAverage,"mAAverage":mAAverage}))
                        db.insertLogData(timeStamp,1,2,sp.get(dayStorage)) #insert log to database
                        pubLogList()#send log list to netpie
                    else:
                        result = False
                        message = "error2"
                        print("Error Arare water")
                else:
                    result = False
                    message = "error1"

                response = json.dumps({"topic":"controlDevice","success":result,"message":message})
                microgear.publish("/response",str(response))
            elif(i == "2"):
                result = False
                message = ""
                if(tm.isShower(timeStamp,tm.getFQDelaySpary())):
                    tB1,tB2,tBAverage =inputs.getTempSet()
                    if(ct.shower()):
                        print("water success")
                        time.sleep(5)
                        tA1,tA2,tAAverage =inputs.getTempSet()
                        if(float(tAAverage)<=float(tBAverage)):
                            print("All success")
                            result = True
                            message = str(json.dumps({"tBAverage":tBAverage,"tAAverage":tAAverage}))
                            db.insertLogData(timeStamp,2,2,sp.get(dayStorage))
                            pubLogList()
                            sp.put(lsShower,int(timeStamp))
                            initSharedPreferences()
                        else:
                            result = False
                            message = "error2"
                            print("Error Atemp decrease")                           
                    else:
                        result = False
                        message = "error1"
                else:
                    result = False
                    message = "error3"
                    print("Error not to time shower")

                response = json.dumps({"topic":"controlDevice","success":result,"message":message})
                microgear.publish("/response",str(response))
            elif(i == "3"):
                result = False
                message = ""
                lB1,lB2,lBAverage = inputs.getLightSet();
                if(ct.openSlat()): #if can close slat
                    time.sleep(5)
                    lA1,lA2,lAAverage = inputs.getLightSet();
                    if(float(lA2)<=float(lB2)): #if light in less than
                        print("all Success")
                        result = True
                        message = str(json.dumps({"lB2":lB2,"lA2":lA2}))
                        sp.put(statusSlat,1) #set slat status to open
                        initSharedPreferences()
                        db.insertLogData(timeStamp,3,2,int(sp.get(dayStorage))) #insert log to database
                        pubLogList() #send log list to netpie
                        pubSTSlat(int(sp.get("statusSlat"))) #send slat status to netpie
                    else:
                        result = False
                        message = "error1"
                        print("Error light in not decrease")
                else:
                    result = False
                    message = "error1"
                    print("Error Slat is open")

                response = json.dumps({"topic":"controlDevice","success":result,"message":message})
                microgear.publish("/response",str(response))
            elif(i == "4"):
                result = False
                message = ""
                if(ct.closeSlat()): #if can open slat
                    print("all Success")
                    result = True
                    sp.put(statusSlat,2) #set slat status to close
                    initSharedPreferences()    
                    db.insertLogData(timeStamp,4,2,int(sp.get(dayStorage)))#insert log to database
                    pubLogList()#send log list to netpie
                    pubSTSlat(int(sp.get("statusSlat")))#send slat status to netpie
                else:
                    result = False
                    message = "error1"
                    print("Error Slat is close")

                response = json.dumps({"topic":"controlDevice","success":result,"message":message})
                microgear.publish("/response",str(response))
        
def callback_present(gearkey) :
    gearkey = gearkey[2:1]
    print ("Main: " +gearkey +" has online.")
    
def callback_absent(gearkey) :
    gearkey = gearkey[2:1]
    print ("Main: " +gearkey +" has offline.")
    
def callback_warning(msg) :
    print ("Main: Warning: " +msg)
    
def callback_info(msg) :
    print ("Main: Info: " +msg)
    
def callback_error(msg) :
    print ("Main: Error: " +msg)
    
#------------Microgear Netpie-----------------------
def initSharedPreferences():
    sp.getSharedPreferences("Memoery")
    
def pubIM():
    inputs.captureImage()
    microgear.publish("/photo",str(timeStamp)+","+str(inputs.cvIM2Base64()),True)
    microgear.publish("/hasPhoto","1")
    sp.put(lsPubImage,timeStamp)
    initSharedPreferences()
    
    
def pubLogList():
    print("publish log list to NETPIE")
    microgear.publish("/logDataList",str(db.selectLogDataList()),True)
    microgear.publish("/hasLogList","1")
    
def pubRawList():
    print("publish raw data list to NETPIE")
    microgear.publish("/rawDataList",str(db.selectRawDataList()),True)
    microgear.publish("/hasRawList","1")
    
def pubSTSlat(st):
    microgear.publish("/STSlat",str(st),True)
    print("publish status slat to NETPIE...")
def pubRawData():
    m1,m2,mAverage = inputs.getMoistureSet()
    t1,t2,tAverage = inputs.getTempSet()
    l1,l2,lAverage = inputs.getLightSet();
    payload = json.dumps({"m1":m1,"m2":m2,"mAverage":m2,"t1":t1,"t2":t2,"tAverage":tAverage,"l1":l1,"l2":l2,"lAverage":lAverage})
    microgear.publish("/rawData",str(payload),True)
    
def onExcep1():
    count1 = int(sp.get(countExcept1))
    count1+=1
    sp.put(count1,countExcept1)
    print("countExcept1: " +str(count1))
    if(int(count1)>int(excepMaxVal)):
        sp.put(timeExcept1,timeStamp)
        sp.put(waitTime1,minAsTimeStamp)
        sp.put(countExcept1,0)
def resetExcept1():
    sp.put(countExcept1,0)
    sp.put(waitTime1,0)
        
def onExcep2(): 
    count2 = int(sp.get(countExcept2))
    count2+=1
    print("countExcept1: " +str(count2))
    if(int(count2)>int(excepMaxVal)):
        sp.put(timeExcept2,timeStamp)
        sp.put(waitTime2,minAsTimeStamp)
        sp.put(countExcept2,0)
def resetExcept2():
    sp.put(countExcept2,0)
    sp.put(waitTime2,0)
def getSlatStatus(l1,l2):
    initSharedPreferences()
    if((int(l1)-int(l2))>1000): #may be has change to 2000 or 3000 ,check in real system
        if(int(sp.get(statusSlat) == 2)):
            return 2
        else:
            sp.put(statusSlat,2)
            return 2
    elif((int(l1)-int(l2))<1000):
        if(int(sp.get(statusSlat)) == 1):
            return 1
        else:
            return int(sp.get(statusSlat))
    else:
        return int(sp.get(statusSlat))

#--------------------------------------------------------------------------------
#Start prgram!!!!

microgear.setalias("Raspberry Pi");
microgear.on_connect = callback_connect
microgear.on_disconnect = callback_disconnect
microgear.on_message = callback_message
microgear.on_present = callback_present
microgear.on_absent = callback_absent
microgear.on_warning = callback_warning
microgear.on_info = callback_info
microgear.on_error = callback_error
microgear.subscribe("/refreshIM")
microgear.subscribe("/settingDetails")
microgear.subscribe("/settingStandard")
microgear.subscribe("/controlDevice")
microgear.subscribe("/token")
microgear.connect()

while True:
    timeStamp = int(time.time())
    m1,m2,mAverage = inputs.getMoistureSet()
    t1,t2,tAverage = inputs.getTempSet()
    l1,l2,lAverage = inputs.getLightSet();
    SlatST = getSlatStatus(l1,l2)
    sp.put(statusSlat,int(SlatST))
    initSharedPreferences()

    print("time: "+str(timeStamp)+" ("+tm.timeStamp2Date(timeStamp)+")")
    print("moistrue1: "+str(m1))
    print("moistrue2: "+str(m2))
    print("temp1: "+str(t1))
    print("temp2: "+str(t2))
    print("light_out: "+str(l1))
    print("light_in: "+str(l2))
    print("slat status: "+str(sp.get(statusSlat)))

    if(tm.isPubRawData(timeStamp)):
        print("publish raw data to NETPIE")
        payload = json.dumps({"m1":m1,"m2":m2,"mAverage":m2,"t1":t1,"t2":t2,"tAverage":tAverage,"l1":l1,"l2":l2,"lAverage":lAverage})
        microgear.publish("/rawData",str(payload),True)
        sp.put(lsPubRawData,timeStamp)
        initSharedPreferences()
    if(tm.isPubImage(timeStamp)):
        print("publish image to NETPIE")
        pubIM()
    if(tm.isInsertRawData(timeStamp)):
        print("insert raw data to database")
        db.insertRawData(timeStamp,mAverage,tAverage,l2)
        sp.put(lsInsertRawData,timeStamp)
        pubRawList()
        
    
    #Smart!!!!!!!!!!
    if(sp.get(autoMode)):
        print("\nOn Work in Auto Mode......")
        if(tm.isDay()):
            print("this time is a day")
            #------------------------------------------------------------------------------------------------
            if(float(mAverage)>0): #if sensor not error
                print("Compare Moisture")
                initSharedPreferences()
                if(float(mAverage)<float(sp.get(moisture))): #if moisture value less than Standard valus
                    if(tm.checkWaitTimeWater(timeStamp)):#if no errors before
                        if(ct.water()): #if water flows
                            print("water success")
                            time.sleep(30)
                            mos1,mos2,mosAverage = inputs.getMoistureSet()
                            if(float(mosAverage)>float(mAverage)):# if moisture value more than valus before
                                print("All success")
                                db.insertLogData(timeStamp,1,1,sp.get(dayStorage)) #insert log to database
                                pubLogList()#send log list to netpie
                                resetExcept1() #reset exception
                            else:
                                print("Error Arare water")
                                onExcep1()#count exception
                        else:
                            print("water false")
                            onExcep1()#count exception
                    else:
                        print("Wait Error")
                else:
                    print("not ting Moisture")
            else:
                print("sensor moisture error")
            #------------------------------------------------------------------------------------------------  
            if(float(tAverage)>0): #if sensor not error
                print("Compare Temp")
                initSharedPreferences()
                if(float(tAverage)>float(sp.get(temp))): #if temparature value more than standard value
                    if(tm.checkWaitTimeShower(timeStamp)):#if no errors before
                        if((float(tAverage)-float(oldTemp))<2): #if present valiue - old value more 2 deegree
                            if(float(oldLight)<=float(l1)): #if light out more than
                                if(tm.isShower(timeStamp,tm.getFQDelaySpary())): #if can shower
                                    if(ct.shower()):
                                        print("water success")
                                        time.sleep(30)
                                        te1,te2,teAverage = inputs.getTempSet()
                                        if(float(teAverage)<=float(tAverage)):#if new temp decrease
                                            print("All success")
                                            db.insertLogData(timeStamp,2,1,sp.get(dayStorage)) #insert log to database
                                            pubLogList()#send log list to netpie
                                            sp.put(lsShower,int(timeStamp)) #set last time to shower
                                            resetExcept2() #reset exception
                                            initSharedPreferences()
                                        else:
                                            onExcep2() #count exception
                                    else:
                                        print("water false")
                                        onExcep2() #count exception
                                else:
                                    print("not time to shower")
                            else:
                                print("relation false!")
                        else:
                            print("sensor may be error or has person distrub")
                    else:
                        print("Wait Error")
                else:
                    print("not ting Temp")  
            else:
                print("sensor temp error")
            #---------------------------------------------------------------------------------------------------
            if(float(l1)>0):#if sensor not error
                print("Compare Light")
                initSharedPreferences()
                if(float(l1)>float(sp.get(light))): #if light out more than light standard value
                    print("Light more than standard")
                    stSlat = sp.get("statusSlat")
                    tm.printSTSlat(stSlat)
                    if(ct.closeSlat()): #if can close slat
                        time.sleep(10)
                        ll1,ll2,llAverage = inputs.getLightSet();
                        if(float(ll2)<float(l2)): #if light in less than
                            print("all Success")
                            sp.put(statusSlat,2) #set slat status to close
                            initSharedPreferences()
                            db.insertLogData(timeStamp,4,1,int(sp.get(dayStorage))) #insert log to database
                            pubLogList() #send log list to netpie
                            pubSTSlat(int(sp.get("statusSlat"))) #send slat status to netpie
                        else:
                            print("for except light....")
                    else:
                        print("")
                else:
                    if((float(sp.get(light))-l1)>2000): #if light out less than standard value more 2000 lux
                        initSharedPreferences()
                        print("Light less than standard")
                        stSlat = sp.get("statusSlat")
                        tm.printSTSlat(stSlat)
                        if(ct.openSlat()): #if can open slat
                            print("all Success")
                            sp.put(statusSlat,1) #set slat status to open
                            initSharedPreferences()
                            db.insertLogData(timeStamp,3,1,int(sp.get(dayStorage)))#insert log to database
                            pubLogList()#send log list to netpie
                            pubSTSlat(int(sp.get("statusSlat")))#send slat status to netpie
                        else:
                            print("")
                    else:
                        print("")
            else:
                print("sensor Light error")
            #----------------------------------------------------------------------------------------------------
        else:
            print("this time is a night")
            if(ct.openSlat()): #if can open slat
                print("all Success")
                sp.put(statusSlat,1) #set slat status to open
                initSharedPreferences()
                db.insertLogData(timeStamp,3,1,int(sp.get(dayStorage))) #insert log to database
                pubLogList()#send log list to netpie
                pubSTSlat(int(sp.get("statusSlat")))#send slat status to netpie
    else:
        print("manual mode....")
    print("------------------------------------")
    oldTemp = tAverage
    oldLight = l1
    time.sleep(5)


