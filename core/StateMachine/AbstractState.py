import time
from core.Debug import Debug

class State:
    name="Abstract State"
    logger=[]
    display=[]

    deltaTime=0
    lastFPSGet=0
    frames=0
    FPS=0

    def __init__(self,name,display,debugLogger=None):
        self.name=name
        self.display=display
        if(debugLogger):
            self.logger=debugLogger
        else:
            self.logger=Debug()
            self.logger.enablePrintConsole=True
            self.logger.logText=self.name
            self.logger.warningText=self.name
            self.logger.errorText=self.name

    def Load(self):
        self.lastFPSGet=time.ticks_ms()

    def Update(self,dt):
        self.deltaTime=dt
        if(time.ticks_diff(time.ticks_ms(), self.lastFPSGet)>1000):
            self.FPS=self.frames
            self.frames=0
            self.lastFPSGet=time.ticks_ms()
    
    def Draw(self):
        self.frames+=1
        self.display.fill(0)