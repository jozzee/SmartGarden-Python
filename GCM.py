from gcm import *
import json
import SharedPreferences as sp

gcm = GCM("AIzaSyA96hbpN4glbpd8VfcZCn0Oia7jPERbDuo")
def setData(title,message):
    return {"body" :message,"title":title,"icon" : "ic_launcher"}
def pushNotification(data):
    print(str(data))
    sp.getSharedPreferences("Memoery")
    reg_id = str(sp.get("token"))
    print(str(reg_id))
    gcm.plaintext_request(registration_id=reg_id,data=data)
    print("pushNotification success")

#pushNotification(setData("Smart Garden Care","Yuor have new message"))

    
