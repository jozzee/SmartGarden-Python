import json
global obj
with open('preferences.txt') as jsonfile:
    global obj
    obj = json.load(jsonfile)
