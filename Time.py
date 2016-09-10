import datetime
import time
import SharedPreferences as sp

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
minAsTimeStamp = 60
hourAsTimeStamp = 3600
waitTime1 = "waitTime1"
waitTime2 = "waitTime2"
timeExcept1 = "timeExcept1"
timeExcept2 = "timeExcept2"
countExcept1 = "countExcept1"
countExcept2 = "countExcept2"
#--------------------------------------------------------------
def initSharedPreferences():
    sp.getSharedPreferences("Memoery")
def getDateTimeAsList():
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dateTime = []
    dateTime.append(date[:-15])#year
    dateTime.append(date[5:-12])#mon
    dateTime.append(date[8:-9])#day
    dateTime.append(date[11:-6])#hour
    dateTime.append(date[14:-3])#min
    dateTime.append(date[17:])#sec
    return dateTime
def cvDT2TimeStamp(dtList):
    t = time.mktime(datetime.datetime(int(dtList[0]),int(dtList[1]),int(dtList[2]),int(dtList[3]),int(dtList[4]),int(dtList[5])).timetuple())
    return str(t).split(".")[0]
def getLSPubRD(frequency):#find last time at pulbish rawData to NETPIE
    initSharedPreferences()
    dateTimeList = getDateTimeAsList()
    if(int(frequency)<60):
            dateTimeList[4] = ((int(dateTimeList[4])//int(frequency))*int(frequency))
            dateTimeList[5] = "00"
    else:
            dateTimeList[4] = "00"
            dateTimeList[5] = "00"

    return cvDT2TimeStamp(dateTimeList)
def getLSIRD(frequency):
    dateTimeList = getDateTimeAsList()
    dateTimeList[3] = ((int(dateTimeList[3])//int(frequency))*int(frequency))
    dateTimeList[4] = "00"
    dateTimeList[5] = "00"
    return cvDT2TimeStamp(dateTimeList)
#--------------------------------------------------------------

initSharedPreferences()
sp.put(lsPubRawData,getLSPubRD(sp.get(fqPubRawData)))
sp.put(lsInsertRawData,getLSIRD(sp.get(fqInsertRawData)))


def getDateTimeNow(): #get datetime on now
    return datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
def timeStamp2Date(timestamp):#convernt timestamp to datetime
    return (datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'))
def isDay():
    hour = datetime.datetime.now().strftime('%H')
    if(int(hour)>6 and int(hour)<18):
        return True
    else:
        return False
def isPubRawData(timeStamp):
    initSharedPreferences()
    if(timeStamp>=(int(sp.get(lsPubRawData))+(int(sp.get(fqPubRawData))*int(minAsTimeStamp)))):
        return True
    else:
        return False
def isPubImage(timeStamp):
    initSharedPreferences()
    if(timeStamp>=(int(sp.get(lsPubImage))+(int(sp.get(fqPubImage))*int(hourAsTimeStamp)))):
        return True
    else:
        return False
def isInsertRawData(timeStamp):
    initSharedPreferences()
    if(timeStamp>=(int(sp.get(lsInsertRawData))+(int(sp.get(fqInsertRawData))*int(hourAsTimeStamp)))):
        return True
    else:
        return False
def isShower(timeStamp,fq):
    initSharedPreferences()
    if(int(timeStamp)>=int(int(sp.get(lsShower))+(int(fq)*int(minAsTimeStamp)))):
        return True
    else:
        return False

def checkWaitTimeWater(timeStamp):
    initSharedPreferences()
    if(int(timeStamp) >= (int(sp.get(timeExcept1))+(int(sp.get(waitTime1))*int(minAsTimeStamp)))):#3660
        return True
    else:
        return False
    
def checkWaitTimeShower(timeStamp):
    initSharedPreferences()
    if(int(timeStamp) >= (int(sp.get(timeExcept2))+(int(sp.get(waitTime2))*int(minAsTimeStamp)))):#3660
        return True
    else:
        return False
def getFQDelaySpary():
    print("getFQDelaySpary")
    if(isDay()):
        month = datetime.datetime.now().strftime('%m')
        hour = datetime.datetime.now().strftime('%H')
        if(int(month)>=3 and int(month)<=5):
            print("hot season")
            if(int(hour)>=6 and int(hour)<=12):
                print("fq: 10 mintue")
                return 10
            elif(int(hour)>=13 and int(hour)<=16):
                print("fq: 3 mintue")
                return 3
            elif(int(hour)>=17 and int(hour)<=18):
                print("fq: 7 mintue")
                return 7
            else:
                print("fq: 0 because is a night")
                return 0
        elif(int(month)>=6 and int(month)<=9):
            print("rain season")
            if(int(hour)>=6 and int(hour)<=12):
                print("fq: 30 mintue")
                return 30
            elif(int(hour)>=13 and int(hour)<=16):
                print("fq: 15 mintue")
                return 15
            elif(int(hour)>=17 and int(hour)<=18):
                print("fq: 20 mintue")
                return 20
            else:
                print("fq: 0 because is a night")
                return 0
        elif((int(month)>=10 and int(month)<=12) or(int(month)>=1 and int(month)<=2)):
            print("hilter")
            if(int(hour)>=6 and int(hour)<=12):
                print("fq: 45 mintue")
                return 45
            elif(int(hour)>=13 and int(hour)<=16):
                print("fq: 20 mintue")
                return 20
            elif(int(hour)>=17 and int(hour)<=18):
                print("fq: 30 mintue")
                return 30
            else:
                print("fq: 0 because is a night")
                return 0
    else:
        return 10
def printSTSlat(stSlat):
    if(stSlat == 1):
        print("slat status: slat is opened")
    elif(stSlat == 2):
        print("slat status: slat is closed")

def getValCTSlat(light_out):
    if((light_out-float(sp.get("light")))>2000):
        return "max"
    else:
        return "halt"
def getValCTSlatOpen(light_out):
    if((float(sp.get("light"))-float(light_out))>2000):
        return "max"
    else:
        return "halt"

