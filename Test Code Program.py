import json
global obj
with open('preferences.txt','r') as jsonfile:
    global obj
    obj = json.load(jsonfile)
    jsonfile.close
