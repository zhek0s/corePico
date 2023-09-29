from ssd1306 import SSD1306_I2C
import framebuf

class Display(SSD1306_I2C):
    MAXIMUM_CHARS_ON_LINE=16
    i2c=[]

    def __init__(self, i2cHandler):
        WIDTH  = 128
        HEIGHT = 64
        self.i2c=i2cHandler
        super().__init__(WIDTH, HEIGHT, self.i2c)

    def getHandler(self):
        return self

    def getI2C(self):
        return self.i2c

    def textAligned(self,text,mod,x,y):
        #R(right),L(Left),C(Center),W(Width)
        #every char on display 8*8 pixels
        if mod=="C":
            textX=x-len(text)*4
            self.text(text,textX,y)
        else:
            print("DRAWING TEXT BY '"+mod+"' MOD NOT SUPPORTED")