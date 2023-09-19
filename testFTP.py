
import network
import time
from core.FTPUpdater.FTPUpdater import FTPUpdater
from lib.display import Display
from machine import Pin, I2C, SPI

#--------------------boot
    
    
#--------------------boot
###########################################
sdaP=Pin(2)
sclP=Pin(3)
i2cHandler=I2C(1, scl=sclP, sda=sdaP, freq=100000)
display=Display(i2cHandler)
spi=SPI(0,2_000_000, mosi=Pin(19),miso=Pin(16),sck=Pin(18))
nic = network.WIZNET5K(spi,Pin(17),Pin(20))
print('Start')
print('Getting ip')
nic.active(True) 
if configPico.ftpUpdate["ftpWork"]:
    time.sleep(3)
    print(nic.ifconfig())
###########################################

#-------------updater
ftpUpdater = FTPUpdater(nic)
ftpUpdater.Update()