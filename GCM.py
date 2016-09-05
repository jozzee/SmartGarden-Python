from gcm import *
import json
import SharedPreferences as sp
sp.getSharedPreferences("Memoery")

gcm = GCM("AIzaSyCmZk_YcNRhEPP2W5HEbMg6SngA9Qt0P6w")
reg_id = "cHXB8_DySSY:APA91bGSjGx2zvNR_xqUFXVmSqaLajm-CV7mSvfe4gWBvh6_Z0nkuFzdntSTuJuCbxger3Ot8gtrUmTa0ysEfm-hxAEOB2dEQnwionIhp5Ze6jYiIt936OxiWdcVQ8HEGkg1SafF6wYN"
def setData(title,message):
    return {"body" :message,"title":title,"icon" : "ic_launcher"}
def pushNotification(data):
    gcm.plaintext_request(registration_id=reg_id,data=data)#str(sp.get("token"))
    print("pushNotification success")



    
