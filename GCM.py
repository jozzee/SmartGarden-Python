from gcm import *
import json
import preference.SharedPreferences as sp
import time

sp.getSharedPreferences()
gcm = GCM("<API Key Google cloud messageing>")

def setData(title,message):
    return {"body" :message,"title":title,"icon" : "ic_launcher"}
def pushNotification(data):
    print("  GCM, pushNotification")

    reg_id = str(sp.get("token"))
    print("    token: "+str(reg_id))
    print("    data: "+str(data))
    try:
        gcm.plaintext_request(registration_id=reg_id,data=data)
        print("    pushNotification success")
    except:
        print("    Opps! has error...")




    
