import network
from machine import Pin,SPI,I2C
from core.Ethernet.w5500PinConfig import W5500PinConfig
from config import ConfigPico

class Ethernet:
    nic=[]
    
    def __init__(self):
        configPin=W5500PinConfig.hard
        spiNum=configPin["spiNum"]
        spiFreq=configPin["spiFreq"]
        spiMosi=configPin["spiMosi"]
        spiMiso=configPin["spiMiso"]
        spiSck=configPin["spiSck"]
        pinSS=configPin["pinSS"]
        pinReset=configPin["pinReset"]
        spi=SPI(spiNum,spiFreq, mosi=Pin(spiMosi),miso=Pin(spiMiso),sck=Pin(spiSck))
        self.nic = network.WIZNET5K(spi,Pin(pinSS),Pin(pinReset)) # type: ignore
        
    def getHandler(self):
        return self.nic
    
    def isConnected(self):
        return self.nic.isconnected() # type: ignore
    
    def activate(self):
        self.nic.active(True) # type: ignore
        
    def deactivate(self):
        self.nic.active(False) # type: ignore

    def ifConfig(self):
        return self.nic.ifconfig() # type: ignore