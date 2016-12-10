import json
import preference.SharedPreferences as sp
import Controls as ctrl
import Inputs as inputs
import GCM as gcm
import Time as t
import time
import Database as db


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

wErrCount = 0
sErrCount = 0
exceptStamp = 3600 #time in unix to working agains (1 hour)
minStamp = 60
errorCount = 3

sp.getSharedPreferences()
ctrl.resetGPIO()

def onExceptWater(timeStamp,errorCode,isConn): # 1 is water false, 2 is arae flase
    global wErrCount
    wErrCount+=1
    print(" count error: "+str(wErrCount))
    if(int(wErrCount)>int(errorCount)):
        print(" has exception!! Water")
        wErrCount = 0
        if(isConn):
            body = json.dumps({"time":timeStamp,"errorCode":errorCode})
            noti = gcm.setData("except",str(body))
            gcm.pushNotification(noti)
        else:
            print("not pushNotification because no internet connection")
        return int(timeStamp)+int(exceptStamp)
    else:
        return 0
    
def onExceptShower(timeStamp,errorCode,isConn): # 3 is water false, 4 temp not declete after working
    global sErrCount
    sErrCount+=1
    print(" count error: "+str(sErrCount))
    if(int(sErrCount)>int(errorCount)):
        print("has exception!! Shower")
        sErrCount = 0
        if(isConn):
            body = json.dumps({"time":timeStamp,"errorCode":errorCode})
            noti = gcm.setData("except",str(body))
            gcm.pushNotification(noti)
        else:
            print("not pushNotification because no internet connection")
        return int(timeStamp)+int(exceptStamp)
    else:
        return 0
    
def compareMosture(timeStamp,mosObj,isConn):
    result = False
    timeExceptWater = 0
    print("Compare, check moisture...")
    
    if(float(mosObj["average"])>0): #if sensor not error  # chamge point1 to average
        if(float(mosObj["average"])<float(sp.get(mosStd))):
            print(" moisture less than standard")
            if(ctrl.water()): 
                time.sleep(30) #wait 30 second
                newMosObj = json.loads(inputs.getMoistureObject())
                print(" old moisture: "+str(mosObj["average"]))# chamge point1 to average
                print(" new moisture: "+str(newMosObj["average"]))# chamge point1 to average
                if((float(newMosObj["point1"]-float(mosObj["average"])>5))):# if moisture value more than valus before  chamge point1 to average
                    print(" All success")
                    db.insertLogData(timeStamp,1,1,float(mosObj["average"]),float(newMosObj["average"])) #insert log to database
                    result = True
                else:
                    print(" Error! water to true Arare")
                    timeExceptWater = onExceptWater(timeStamp,2,isConn)
            else:
                print(" Error! water not flows")
                timeExceptWater = onExceptWater(timeStamp,1,isConn)
        else:
            print(" no working...")
    else:
        print(" moisture sensor error!!")

    return result,timeExceptWater
    

    
def compareTemp(timeStamp,temObj,lastTimeShower,isConn,mosObj,stSlat,ligObj):
    result = False
    timeExceptShower = 0
    print("Compare, check temp...")
    if(float(temObj["point1"])>0): # chamge point1 to average
        if(float(temObj["average"])>float(sp.get(tmpStd))): # chamge point1 to average
            fq = sp.get(fqShower)
            if(fq == 0):
                fq = t.getFqShower()#get ferquency from system (fq in minute *60) minStamp
            print(" ferquency: "+str(fq) +" minute")
            if(int(timeStamp)>=(int(lastTimeShower)+(int(fq)*int(minStamp)))):
                if(float(mosObj["average"]) <= float(sp.get(mosStd))):#dgfbndgfnhdgnmhjmk
                    if(ctrl.shower()):
                        time.sleep(30) #wait 30 seccond
                        newTemObj = json.loads(inputs.getTempObject())
                        print(" old temp: "+str(temObj["average"])) # chamge point1 to average
                        print(" new temp: "+str(newTemObj["average"])) # chamge point1 to average
                        if(float(newTemObj["point1"])<=float(temObj["average"])): # chamge point1 to average 
                            print(" All success")
                            db.insertLogData(timeStamp,2,1,float(temObj["average"]),float(newTemObj["average"])) #insert log to database # chamge point1 to average
                            result = True
                        else:
                            print(" Error! temp not decrease after shower")
                            timeExceptShower = onExceptShower(timeStamp,3,isConn)   
                    else:
                        print(" Error! water not flows")
                        timeExceptShower = onExceptShower(timeStamp,1,isConn)
                else:
                    if(int(stSlat) == 1): #close slat
                        ligIn = float(ligObj["light_in"])
                        ligOut = float(ligObj["light_out"])
                        if(ctrl.closeSlat()): #if can close slat
                            time.sleep(10)
                            newLigObj = json.loads(inputs.getLightObject())
                            if(float(newLigObj["light_in"]) > float(ligIn)):
                                print("  but new light value not decrease")
                                if(isConn):
                                    noti = gcm.setData("except",str(7))
                                    gcm.pushNotification(noti)
                            db.insertLogData(timeStamp,4,1,float(ligIn),float(newLigObj["light_in"])) #insert log to database   
                            sp.put(slatStatus,str("0"))
                            result = True
                    else:
                        if(ctrl.shower()):
                            time.sleep(30) #wait 30 seccond
                            newTemObj = json.loads(inputs.getTempObject())
                            print(" old temp: "+str(temObj["average"])) # chamge point1 to average
                            print(" new temp: "+str(newTemObj["average"])) # chamge point1 to average
                            if(float(newTemObj["point1"])<=float(temObj["average"])): # chamge point1 to average 
                                print(" All success")
                                db.insertLogData(timeStamp,2,1,float(temObj["average"]),float(newTemObj["average"])) #insert log to database # chamge point1 to average
                                result = True
                            else:
                                print(" Error! temp not decrease after shower")
                                timeExceptShower = onExceptShower(timeStamp,3,isConn)   
                        else:
                            print(" Error! water not flows")
                            timeExceptShower = onExceptShower(timeStamp,1,isConn)   
            else:
                print(" not time to shower, Working again at "+t.timeStampToDateTime((int(lastTimeShower)+(int(fq)*int(minStamp))))) 
        else:
            print(" no working...")    
    else:
        print(" temp sensor error!!")
    
    return result,timeExceptShower
    
def compareLight(timeStamp,ligObj,st,isConn):
    result = False
    std = float(sp.get(ligStd))
    ligIn = float(ligObj["light_in"])
    ligOut = float(ligObj["light_out"])
    
    print("Compare, check light...")
    
    if((ligIn > 0) and (ligOut > 0)):
        if((ligIn > std) and (ligOut > std)):
            print(" light more than standard")
            if(st != 0):
                if(ctrl.closeSlat()): #if can close slat
                    time.sleep(10)
                    newLigObj = json.loads(inputs.getLightObject())
                    if(float(newLigObj["light_in"]) > float(ligIn)):
                       print("  but new light value not decrease")
                       if(isConn):
                           noti = gcm.setData("except",str(7))
                           gcm.pushNotification(noti)
                db.insertLogData(timeStamp,4,1,float(ligIn),float(newLigObj["light_in"])) #insert log to database   
                sp.put(slatStatus,str("0"))
                result = True
                st = 0
            else:
                print(" but slat is closed (0)")
        elif((ligIn < std) and (ligOut < std)):
            print(" light lessthan standard")
            if(st != 1):
                if(ctrl.openSlat()):#if can open slat
                    time.sleep(10)
                    newLigObj = json.loads(inputs.getLightObject())
                    db.insertLogData(timeStamp,3,1,float(ligIn),float(newLigObj["light_in"])) #insert log to database   
                    sp.put(slatStatus,int(1))
                    result = True
                    st = 1  
            else:
                print(" but slat is opened (1)")
    elif(float(ligObj["light_in"]) >0):
        print(" light out error, Compare in one sensor mode")
        if(ligIn > std): #close slat
            print(" light more than standard")
            if(st != 0):
                if(ctrl.closeSlat()): #if can close slat
                    time.sleep(10)
                    newLigObj = json.loads(inputs.getLightObject())
                    if(float(newLigObj["light_in"]) > float(ligIn)):
                       print("  but new light value not decrease")
                       if(isConn):
                           noti = gcm.setData("except",str(5))
                           gcm.pushNotification(noti)
                db.insertLogData(timeStamp,4,1,float(ligIn),float(newLigObj["light_in"])) #insert log to database   
                sp.put(slatStatus,str("0"))
                result = True
                st = 0
            else:
                print(" but slat is closed (0)")
            
        elif((std - ligIn) > 2000): #open slat
            print(" light lessthan standard ever 2,000 lux")
            if(st != 1):
                if(ctrl.openSlat()):#if can open slat
                    time.sleep(10)
                    newLigObj = json.loads(inputs.getLightObject())
                    db.insertLogData(timeStamp,3,1,float(ligIn),float(newLigObj["light_in"])) #insert log to database   
                    sp.put(slatStatus,int(1))
                    result = True
                    st = 1  
            else:
                print(" but slat is opened (1)")
                
    else:
        print(" light sensor error!!")
    return result,st

