import base64
def cvIM2Base64():
      with open("image/garden.jpg","rb") as imageFile:
            imageAsString = base64.b64encode(imageFile.read())
      return imageAsString.decode('utf-8')
