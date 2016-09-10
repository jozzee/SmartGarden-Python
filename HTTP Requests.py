import requests
import json
import SharedPreferences as sp
sp.getSharedPreferences("Memoery")

data = {"data":{"test2":2,"test1":1},"to":str(sp.get("token"))}
response = requests.post("https://fcm.googleapis.com/fcm/send",data=json.dumps(data),headers={'Authorization':'key=AIzaSyDPak_-E7ZPheoNLu8_imsQ99sb2YdMrtw','Content-Type':'application/json'})
print(response.text)
