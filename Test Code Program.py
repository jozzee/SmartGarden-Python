import json
global obj
with open('preferences.txt', 'w') as outfile:
    json.dump(obj, outfile)
    outfile.close
