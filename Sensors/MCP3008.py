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

def subDecimal(val):
    sub =  val.split(".")
    if(len(sub)==2):
        sub[1] = (sub[1])[:2]
        return(sub[0]+"."+sub[1])
    else:
        return val

def readMoisture(addr):
    hu = mcp.read_adc(addr)
    if(hu > 1023) or (hu < 1):
        humidity = -1
    else:
        humidity = subDecimal(str((float(100)-(float(hu)/float(10.24)))))   
    return(float(humidity))

def redAsDigit(addr):
    return mcp.read_adc(addr)

def readMostureAsVoltage():
    hu = mcp.read_adc(0)
    humidity = (float(3.3)/(float(1024)/float(hu)))
    return(humidity)

