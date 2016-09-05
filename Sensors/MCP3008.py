import time
# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008


# Software SPI configuration:
#CLK  = 18
#MISO = 23
#MOSI = 24
#CS   = 25
#mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

#Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

def readMoisture(addr):
    hu = mcp.read_adc(addr)
    #print("MCP3008: "+str(hu))
    #print("hu: "+str(hu))
    if(hu > 1013) or (hu < 11):
        humidity = -1
    else:
        humidity = (float(100)-(float(hu)/float(10.24)))
    #print("MCP3008, humidity: "+str(humidity) +" %")
    return(humidity)

def readMostureAsVoltage():
    hu = mcp.read_adc(0)
    humidity = (float(3.3)/(float(1024)/float(hu)))
    print("MCP3008, voltage: "+str(humidity)+" volt")
    return(humidity)
#while True:
#    print(str(readMoisture(0)))
#    time.sleep(1)
    
