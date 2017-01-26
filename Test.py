def get(key):
    getSharedPreferences()
    if(obj != None):
        for r in obj:
            if(key in r):
                return obj[key]
