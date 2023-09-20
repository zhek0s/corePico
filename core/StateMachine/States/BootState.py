import time
import framebuf
from core.StateMachine.AbstractState import State
from core.StateMachine.commonUI import CommonUI

class BootState(State):

    picoImage=[]
    picoImageX=0
    picoImageV=1

    def __init__(self,display):
        super().__init__("BootState",display)

    def Load(self):
        super().Load()
        buffer = CommonUI.images["pico32*32"]
        self.picoImage = framebuf.FrameBuffer(buffer, 32, 32, framebuf.MONO_HLSB)

    def Update(self,dt):
        super().Update(dt)
    
    def Draw(self):
        super().Draw()
        self.display.text("CPU dt:"+str(self.deltaTime),0,0)
        self.display.text("FPS:"+str(self.FPS),0,10)
        if(self.picoImageX>95):
          self.picoImageV=-1
        elif(self.picoImageX<1):
          self.picoImageV=1
        self.picoImageX+=self.picoImageV
        self.display.blit(self.picoImage, self.picoImageX, 32)
        self.display.show()
    