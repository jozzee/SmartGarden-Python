import datetime
import time

minuteStamp =  60 # 1 mintue in time stamp
hourStamp = 3600 # 1 hour in time stamp
exceptStamp = 3600 #waite time for working agens after has exception (is 1 hour in time stamp)

def getDateTime():
    return datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
def isDay():
    hour = datetime.datetime.now().strftime('%H')
    if(int(hour)>6 and int(hour)<18):
        return True
    else:
        return False
def getTimeAsArray():
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    arr = []
    arr.append(date[:-15])#year
    arr.append(date[5:-12])#mon
    arr.append(date[8:-9])#day
    arr.append(date[11:-6])#hour
    arr.append(date[14:-3])#min
    arr.append(date[17:])#sec
    return arr
def timeArrayToTimeStamp(timeArray):
    t = time.mktime(datetime.datetime(int(timeArray[0]),int(timeArray[1]),int(timeArray[2]),int(timeArray[3]),int(timeArray[4]),int(timeArray[5])).timetuple())
    return str(t).split(".")[0]
def timeStampToDateTime(timeStamp):
    if(timeStamp == ""):
        return (datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
    else:
        return (datetime.datetime.fromtimestamp(int(timeStamp)).strftime('%Y-%m-%d %H:%M:%S'))

def getNextTimePubData(fq): #fq = frequency in minute unit, LP = Last Publish
    timeArray = getTimeAsArray()
    if(int(fq)<60):
        timeArray[4] = ((int(timeArray[4])//int(fq))*int(fq))
        timeArray[5] = "00"
    else:
        timeArray[4] = "00"
        timeArray[5] = "00"
    ls = timeArrayToTimeStamp(timeArray)
    return int(int(ls)+(int(fq)*int(minuteStamp)))

def getNextTimeInsertData(fq):#fq = frequency in hour unit, LI = Last Insert
    timeArray = getTimeAsArray()
    timeArray[3] = ((int(timeArray[3])//int(fq))*int(fq))
    timeArray[4] = "00"
    timeArray[5] = "00"
    ls = timeArrayToTimeStamp(timeArray)
    return int(int(ls)+(int(fq)*int(hourStamp)))

def canPublishData(timeStamp,lPData,fq):
    if(int(timeStamp)>=(int(lPData)+(int(fq)*int(minuteStamp)))):
        return True
    else:
        return False
def canPublishImage(timeStamp,lPImage,fq):
    if(int(timeStamp)>=(int(lPImage)+(int(fq)*int(hourStamp)))):
        return True
    else:
        return False
def canInsertData(timeStamp,lIData,fq):
    if(int(timeStamp)>=(int(lIData)+(int(fq)*int(hourStamp)))):
        return True
    else:
        #print("not time to insert database, can insert data at: "+timeStampToDateTime(int(lIData)+(int(fq)*int(hourStamp))))
        return False
def getSesion():
    sesion = 0 #1 is hot, 2 is rain, 3 is clod
    m = datetime.datetime.now().strftime('%m')
    d = datetime.datetime.now().strftime('%d')
    if((int(m)>=2) and (int(m)<=5)):
        if(int(m) == 2):
            if(int(d)>15):
                sesion = 1
            else:
                sesion = 3
        elif(int(m) == 5):
            if(int(d)<15):
                sesion = 1
            else:
                sesion = 2
        else:
            sesion = 1
    elif((int(m)>=5)and(int(m)<=10)):
        if(int(m) == 5):
            if(int(d)>15):
                sesion = 2
            else:
                sesion = 1
        elif(int(m) == 10):
            if(int(d)<15):
                sesion = 2
            else:
                sesion = 3
        else:
            sesion = 2
    elif((int(m)>=10)or(int(m)<=2)):
        if(int(m) == 10):
            if(int(d)<15):
                sesion = 3
            else:
                sesion = 2
        elif(int(m) == 2):
            if(int(d)<15):
                sesion = 3
            else:
                sesion = 1
        else:
            sesion = 3

    return sesion
def getMorningAfternoon():
    h = datetime.datetime.now().strftime('%H')
    if((int(h)>=6) and (int(h)<=18)):
        if(int(h)<=9):
            return 1 #morning
        elif(int(h)<=12):
            return 2 #noon
        elif(int(h)<=16):
            return 3 #afternoon
        else:
            return 4 #evening
    else:
        return 0; # is a night
    
def getFqShower():
    sesion = getSesion()
    t = getMorningAfternoon()
    fq = 10
    if(int(t)>0):
        if(int(t)== 1): #
            if(int(sesion) == 1): 
                fq = 5 #morning in hot
            elif(int(sesion) == 2):
                fq = 8 #morning in rain
            elif(int(sesion) == 3):
                fq = 10 #morning in clod
        if(int(t)== 2):
            if(int(sesion) == 1):
                fq = 3 #noon in hot
            elif(int(sesion) == 2):
                fq = 5 #noon in rain
            elif(int(sesion) == 3):
                fq = 8 #noon in clod
        if(int(t)== 3):
            if(int(sesion) == 1):
                fq = 1 #afternoon in hot
            elif(int(sesion) == 2):
                fq = 5 #afternoon in rain
            elif(int(sesion) == 3):
                fq = 10 #afternoon in clod
        if(int(t)== 4):
            if(int(sesion) == 1):
                fq = 10 #evening in hot
            elif(int(sesion) == 2):
                fq = 12 #evening in rain
            elif(int(sesion) == 3):
                fq = 15 #evening in clod
            print("")
    return fq
def canShower(timeStamp,lShower):
    fq = getFqShower()
    if((int(timeStamp))>=(int(lShower)+(int(fq)*(minuteStamp)))):
        return True,0,0
    else:
        return False,(int(lShower)+(int(fq)*(minuteStamp))),fq #return canShower, nextTime to can, frequency
def hasExceptWater(timeStamp,timeExcept):
    if(int(timeExcept)>0):
        if(int(timeStamp)>=(int(timeExcept)+int(exceptStamp))):
            return False
        else:
            return True
    else:
        return False
def isExceptShower(timeStamp,timeExcept):
    if(int(timeExcept)>0):
        if(int(timeStamp)>=(int(timeExcept)+int(exceptStamp))):
            return False
        else:
            return True
    else:
        return False

