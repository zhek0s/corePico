from machine import Pin, I2C
import time
from picozero import Button

class TH06:

    def __init__(self, i2cHandler):
        self.th06addr = 0x40
        self.i2c = i2cHandler
        print(self.i2c.scan())
        th06addr=self.i2c.scan()[0]
        print(th06addr)

    def GetTempHum(self):
        bytes=self.i2c.readfrom_mem(self.th06addr, 0xE3, 2)
        value=int.from_bytes(bytes,"big")
        temp=(175.2*value)/65536 - 46.85
        bytes=self.i2c.readfrom_mem(self.th06addr, 0xE5, 2)
        value=int.from_bytes(bytes,"big")
        hum=(125*value)/65536 - 6
        print("Temp: "+str(temp))
        print("Hum:  "+str(hum))
        return temp,hum

#define TH06_I2C_DEV_ID               0x40
#define TH06_Humi_Hold_Master_Mode    0xE5
#define TH06_Humi_No_Hold_Master_Mode 0xF5
#define TH06_Temp_Hold_Master_Mode    0xE3
#define TH06_Temp_No_Hold_Master_Mode 0xF3
#define TH06_Reset                    0xFE
#define TH06_WR_RH                    0xE6
#define TH06_RD_RH                    0xE7
#define TH06_RTV_from_PRM             0xE0