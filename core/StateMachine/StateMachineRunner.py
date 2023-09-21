import time
from core.StateMachine.AbstractState import State

class StateMachineRunner:
    
    logger=[]
    state=State("abstract",[])
    running=False

    lastTimeRunning=0
    lastTimeDrawing=0
    lock60fps=True
    drawingFreq=60
    drawingDelay=1000/drawingFreq
    
    def __init__(self,debugLogger):
        self.logger=debugLogger
        self.logger.enablePrintConsole=True
        self.logger.logText="StateMachineRunner"
        self.logger.warningText="StateMachineRunner"
        self.logger.errorText="StateMachineRunner"
        self.logger.log("Started")
        self.running=False
        
    def setState(self,state):
        self.state=state
        self.logger.log("Change state to "+state.name)
        self.logger.log("Call Load from "+state.name)
        self.state.Load()
        self.running=True
        lastTimeRunning=time.ticks_ms()
        lastTimeDrawing=time.ticks_ms()

    def Update(self):
        if(self.running):
            dt=time.ticks_diff(time.ticks_ms(), self.lastTimeRunning)
            self.state.Update(time.ticks_diff(time.ticks_ms(), self.lastTimeRunning))
            self.lastTimeRunning=time.ticks_ms()
            if(self.lock60fps):
                if(time.ticks_diff(time.ticks_ms(), self.lastTimeDrawing)>self.drawingDelay):
                    self.lastTimeDrawing=time.ticks_ms()
                    self.state.Draw()
            else:
                self.state.Draw()

