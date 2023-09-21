import time
import framebuf
from machine import Timer
from core.StateMachine.AbstractState import State
from core.StateMachine.commonUI import CommonUI
from core.CoreVersion import Versions

class BootState(State):

    bootStage=0
    bootStageChanged=True
    tim=[]

    picoImage=[]
    picoImageX=48
    picoImageY=0

    def __init__(self,display):
        super().__init__("BootState",display)

    def Load(self):
        super().Load()
        buffer = CommonUI.images["pico32*32"]
        self.picoImage = framebuf.FrameBuffer(buffer, 32, 32, framebuf.MONO_HLSB)
        self.display.blit(self.picoImage, self.picoImageX, self.picoImageY)
        self.bootStage=1
        #ethernet=Ethernet()
        #ethernet.activate()
        #nic=ethernet.getHandler()
        #time.sleep(3)
        #print(nic.ifconfig())

    def Update(self,dt):
        super().Update(dt)
        self.microStageRunner()
    
    def Draw(self):
        super().Draw()
        self.display.text(str(self.deltaTime),0,0)
        self.display.text(str(self.FPS),0,10)
        self.display.blit(self.picoImage, self.picoImageX, self.picoImageY)
        self.microStageDraw()
        self.display.show()
        

    def stageChangerCallback(self,newVal):
        self.bootStage=newVal
    
    def microStageRunner(self):
        if self.bootStage==1:
            if(self.bootStageChanged):
                self.tim = Timer(period=3000, mode=Timer.ONE_SHOT, callback=lambda t:self.stageChangerCallback(2))
                self.bootStageChanged=False
            else:
                time.sleep_ms(1)
        elif self.bootStage==2:
            time.sleep_ms(1)
        else:
            if(self.bootStageChanged):
                print("not set stage")
                self.bootStageChanged=False
            else:
                time.sleep_ms(1)

    def microStageDraw(self):
        if self.bootStage==1:
            self.display.textAligned("Core "+Versions.coreVersion,"C",64,56)
        elif self.bootStage==2:
            self.display.textAligned("Other boot operations","C",64,56)
        else:
            self.display.textAligned("not set stage","C",64,56)

