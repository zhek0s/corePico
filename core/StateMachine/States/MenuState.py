import time
import framebuf
import json
from core.StateMachine.commonUI import CommonUI
from core.StateMachine.AbstractState import State
from lib.th06 import TH06

class MenuState(State):
    
    th06: TH06
    thLastRead=0
    thReadDelay=2000
    temp=0
    hum=0
    
    mqtt=[]
    mqttLastWrite=0
    mqttWriteDelay=2000
    thPublish={
        'payload':{
            'Temp':{
                'val':'idk :('
                },
            'Hum':{
                'val':'idk'
                }
            }
        }

    def __init__(self,display,mqtt):
        super().__init__("BootState",display)
        self.mqtt=mqtt

    def Load(self):
        super().Load()
        self.th06=TH06(self.display.getI2C())
        buffer = CommonUI.images["main"]
        self.picoImage = framebuf.FrameBuffer(buffer, 128, 64, framebuf.MONO_HLSB)
        self.display.blit(self.picoImage, 0, 0)
        self.thLastRead=time.ticks_ms()

    def Update(self,dt):
        super().Update(dt)
        if(time.ticks_diff(time.ticks_ms(), self.thLastRead)>self.thReadDelay):
            self.temp,self.hum=self.th06.GetTempHum()
            self.thLastRead=time.ticks_ms()
        if(time.ticks_diff(time.ticks_ms(), self.mqttLastWrite)>self.mqttWriteDelay):
            self.thPublish['payload']['Temp']['val']=self.temp
            self.thPublish['payload']['Hum']['val']=self.hum
            self.mqtt.publish(json.dumps(self.thPublish))
            print("send")
            self.mqttLastWrite=time.ticks_ms()
        time.sleep_ms(10)
    
    def Draw(self):
        super().Draw()
        self.display.blit(self.picoImage, 0, 0)
        self.display.text(str(time.localtime()[3]),67,2)
        self.display.text(str(time.localtime()[4]),88,2)
        self.display.text(str(time.localtime()[5]),109,2)
        self.display.text(str(self.temp),109,23)
        self.display.text(str(self.hum),109,39)
        self.display.show()
   