import datetime
import time
def isDay():
    hour = datetime.datetime.now().strftime('%H')
    if(int(hour)>6 and int(hour)<18):
        return True
    else:
        return False
