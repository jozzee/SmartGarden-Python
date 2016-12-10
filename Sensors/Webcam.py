import base64
import picamera
import os

def cvIM2Base64():#cv: convernt
    with open("<Path of image>/garden.jpg","rb") as imageFile:
        imageAsString = base64.b64encode(imageFile.read())
    return imageAsString.decode('utf-8')

def captureImage():
    os.system("fswebcam -r 1280x720 --no-banner /<Path of image>/garden.jpg")
