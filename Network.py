import socket

REMODE_SERVER = "www.google.com"

def isConnectInternet():
    try:
        host = socket.gethostbyname(REMODE_SERVER)
        s = socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False

