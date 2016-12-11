import microgear.client as microgear
import time
microgear.create(<gearkey>,<gearsecret>, <appid>,{'debugmode': True})
def connection():
      print("Now I am connected with netpie")
def subscription(topic,message):
      print(topic+" "+message)
def disconnect():
      print("disconnected")
microgear.setalias("Raspberry Pi Python")
microgear.on_connect = connection
microgear.on_message = subscription
microgear.on_disconnect = disconnect
microgear.subscribe("/token")
microgear.subscribe("/refresh")
microgear.subscribe("/settingStandard")
microgear.subscribe("/settingDetails")
microgear.subscribe("/controlDevieces")
microgear.subscribe("/alarm")
microgear.connect()
