import datetime
import time
import json
import Inputs as inputs
import preference.SharedPreferences as sp
import Database as db
import Time as t
import Controls as ctrl

global alarmList

def controlsDevices(working):
    success = False
    data = ""
    if(working == 1):
        print(" Water from alarm clock")
        mosObj = json.loads(inputs.getMoistureObject())
        if(ctrl.water()):
            time.sleep(30) #wait 30 second
            newMosObj = json.loads(inputs.getMoistureObject())
            print("  old moisture: "+str(mosObj["average"]))
            print("  new moisture: "+str(newMosObj["average"]))
            if((float(newMosObj["average"]-float(mosObj["average"])>5))):# if moisture value more than valus before
                result = db.insertLogData(int(time.time()),1,3,float(mosObj["average"]),float(newMosObj["average"])) #insert log to database
                if(result):
                    print("  All success")
                    success = True
                    data = {"valBefore":float(mosObj["average"]),"valAfter":float(newMosObj["average"])}
                else:
                    data = {"errorCode":0,"msg":"database error","valBefore":float(mosObj["average"]),"valAfter":float(newMosObj["average"])}
            else:
                print("  Error! water not true Arare")
                data = {"errorCode":2,"msg":"water not true arare"}
        else:
            print("  Error! water not flows")
            data = {"errorCode":1,"msg":"water not flows"}
    elif(working == 2):
        print(" Shower from alarm clock")
        temObj = json.loads(inputs.getTempObject())
        if(ctrl.shower()):
            time.sleep(20)
            newTemObj = json.loads(inputs.getTempObject())
            print("  old temp: "+str(temObj["average"]))
            print("  new temp: "+str(newTemObj["average"]))
            if(float(newTemObj["average"])<=float(temObj["average"])):
                result = db.insertLogData(int(time.time()),2,3,float(temObj["average"]),float(newTemObj["average"])) #insert log to database
                if(result):
                    success = True
                    data = {"valBefore":float(temObj["average"]),"valAfter":float(newTemObj["average"])}
                    print("  All success")
                    sp.put("lastTimeShower",int(time.time()))
            else:
                print(" Error! temp not decrease after shower")
                data = {"errorCode":3,"msg":"temp not decrease after shower"}
        else:
            print(" Error! water not flows")
            data = {"errorCode":1,"msg":"water not flows"}
       
    elif(working == 3):
        print(" Open slat from alarm clock")
        slatStatus = sp.get("slatStatus")   #status of slat
        print("  slatStatus: " +str(slatStatus))
        if(int(slatStatus) != 1):
            ligObj = json.loads(inputs.getLightObject())
            if(ctrl.openSlat()):#if can open slat
                time.sleep(20)
                newLigObj = json.loads(inputs.getLightObject())
                sp.put("slatStatus",str("1"))
                result = db.insertLogData(int(time.time()),3,3,float(ligObj["light_in"]),float(newLigObj["light_in"])) #insert log to database
                if(result):
                    success = True
                    data = {"valBefore":float(ligObj["light_in"]),"valAfter":float(newLigObj["light_in"])}
                    print("  All success")
                else:
                    data = {"errorCode":0,"msg":"database error","valBefore":float(ligObj["light_in"]),"valAfter":float(newLigObj["light_in"])}         
        else:
            print("  slat is opened (1)")
            data = {"errorCode":5,"msg":"slat is opened"}
        print(str(data))
    elif(working == 4):
        print(" Close slat from alarm clock")
        slatStatus = sp.get("slatStatus")   #status of slat
        print("  slatStatus: " +str(slatStatus))
        if(int(slatStatus) != 0):
            ligObj = json.loads(inputs.getLightObject())
            if(ctrl.closeSlat()): #if can close slat
                time.sleep(20)
                newLigObj = json.loads(inputs.getLightObject())
                print("  old light: "+str(ligObj["light_in"]))
                print("  new light: "+str(newLigObj["light_in"]))
                
                sp.put("slatStatus",str("0"))
                result = db.insertLogData(int(time.time()),4,3,float(ligObj["light_in"]),float(newLigObj["light_in"])) #insert log to database
                if(result == False):
                    data = {"errorCode":0,"msg":"database error","valBefore":float(ligObj["light_in"]),"valAfter":float(newLigObj["light_in"])}
                if(float(newLigObj["light_in"]) < float(ligObj["light_in"])):
                    success = True
                    data = {"valBefore":float(ligObj["light_in"]),"valAfter":float(newLigObj["light_in"])}
                else:
                    print("  new light value not decrease")
                    data = {"errorCode":7,"msg":"light value not decrease"}
        else:
            print("  slat is closed (0)")
            data = {"errorCode":6,"msg":"slat is closed"}

    return success,data
def getAlarmList():
    try:
        with open('/preference/alarm.txt') as jsonFile:
            global alarmList
            alarmList = json.load(jsonFile)
        return alarmList
    except ValueError:
        print("Opps! Error load JSON File")
def setAlarmToText(payload):
    try:
        with open('/preference/alarm.txt', 'w') as outfile:
             json.dump(payload, outfile)
        getAlarmList()
    except ValueError:
        print("Opps! Error uot file")

def haveAlarmClock():
    have = False
    body = ""
    count = 0
    for alarm in alarmList:
        print("alarm: "+str((int(count)+1)))
        isOpen = bool(alarm["isOpen"])
        print(" isOpen: "+str(isOpen))
        if(isOpen):
            thisHour = int(datetime.datetime.now().strftime('%H'))
            thisMin = int(datetime.datetime.now().strftime('%M'))
            print(" this time: "+str(thisHour)+":"+str(thisMin))
            print(" alarm time: "+str(alarm['hour'])+":"+str(alarm['minute']))
            if((thisHour == int(alarm['hour'])) and (thisMin == int(alarm['minute']))):
                print(" Have Alarm Clock!!")
                isRepeat = bool(alarm['isRepeat'])
                if(isRepeat):
                    print(" Repeat")
                    thisDay = str(datetime.datetime.now().strftime('%a'))
                    daySet = alarm['daysSet']
                    for d in daySet:
                        if(thisDay == d):
                            working = int(alarm['working'])
                            success,data = controlsDevices(working)
                            body = json.dumps({"working":working,"success":success,"data":data,"time":(str(alarm['hour'])+":"+str(alarm['minute']))})
                            have = True
                else:
                    working = int(alarm['working'])
                    success,data = controlsDevices(working)
                    flag = {"index":count,"isOpen":False}
                    body = json.dumps({"working":working,"success":success,"data":data,"flag":flag,"time":(str(alarm['hour'])+":"+str(alarm['minute']))})
                    alarmList[count]['isOpen'] = False
                    setAlarmToText(alarmList)
                    have = True
    return have,body



