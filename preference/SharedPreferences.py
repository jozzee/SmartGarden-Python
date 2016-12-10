#/usr/bin/pythonw
# encoding=utf8
import json
global obj

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

def getSharedPreferences():
    #print("Preferences, getSharedPreferences")
    try:
        with open('/var/www/html/smartgarden/programs/preference/preferences.txt') as jsonfile:
            global obj
            obj = json.load(jsonfile)
        return obj
    except ValueError:
        print("Oops! Error load JSON file")
def commit():
    with open('/var/www/html/smartgarden/programs/preference/preferences.txt', 'w') as outfile:
        json.dump(obj, outfile)
def get(key):
    getSharedPreferences()
    if(obj != None):
        for r in obj:
            if(key in r):
                return obj[key]
def put(key,value):
    a_dict = {key:value}
    global obj
    obj[key] = value
    obj.update(a_dict)
    commit()
    #print(obj[key])
def getVersionData():
    if(obj != None):
        return int(obj[lastUpdate])
def setSharedPreferences(newObj):
    if(obj != None):
        if(getVersionData() < int(newObj[lastUpdate])):
            print("\nPreference, has new update setSharedPreferences")
            for i in newObj:
                print(" "+str(i) +": "+str(newObj[i]))
                put(str(i),newObj[i])

