#/usr/bin/pythonw
# encoding=utf8

import json

global obj
global spName

def getSharedPreferences(preferences):
    global spName
    spName = preferences
    with open(str(preferences+'.txt')) as jsonfile:
        global obj
        obj = json.load(jsonfile)
    return obj

def get(key):
    for r in obj:
        if(key in r):
            return obj[key]

def commit():
    if(spName):
        #print(spName)
        with open(str(spName+'.txt'), 'w') as outfile:
            json.dump(obj, outfile)
    else:
        print("exception: not have file name")

def put(key,value):
    a_dict = {key:value}
    obj[key] = value
    obj.update(a_dict)
    commit()
    #print(obj[key])



