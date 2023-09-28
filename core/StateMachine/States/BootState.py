import time
import framebuf
from machine import Timer
from core.Debug import Debug
from core.FTPUpdater.FTPUpdater import FTPUpdater
from core.StateMachine.AbstractState import State
from core.StateMachine.commonUI import CommonUI
from core.CoreVersion import Versions
from core.Ethernet.Ethernet import Ethernet

class BootState(State):

    bootStage=0
    bootStageChanged=True
    drawingTextLine1="sometext"
    drawingTextLine2="sometext"
    tim=[]

    picoImage: framebuf.FrameBuffer
    picoImageX=48
    picoImageY=0

    ethernet: Ethernet
    nic=[]
    isInitEthernet=False
    needIPEthernet=True

    isInitFTPUpdater=False
    needDoneFTPUpdater=True
    isThreadRunningFTPUpdater=False
    logFTPUpdater=["Started"]

    def __init__(self,display):
        super().__init__("BootState",display)

    def Load(self):
        super().Load()
        buffer = CommonUI.images["pico32*32"]
        self.picoImage = framebuf.FrameBuffer(buffer, 32, 32, framebuf.MONO_HLSB)
        self.display.blit(self.picoImage, self.picoImageX, self.picoImageY)
        self.bootStage=1

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
        self.bootStageChanged=True
    
    def microStageRunner(self):
        if self.bootStage==1:
            if(self.bootStageChanged):
                self.tim = Timer(period=3000, mode=Timer.ONE_SHOT, callback=lambda t:self.stageChangerCallback(2))
                self.bootStageChanged=False
            else:
                time.sleep_ms(1)
        elif self.bootStage==2:
            self.logicStageEthernet()
        elif self.bootStage==3:
            self.logicStageFTPUpdater()
        else:
            if(self.bootStageChanged):
                self.bootStageChanged=False
            else:
                time.sleep_ms(1)

    def microStageDraw(self):
        if self.bootStage==1:
            self.display.textAligned("Core "+Versions.coreVersion,"C",64,56)
        elif self.bootStage==2:
            self.display.textAligned(self.drawingTextLine1,"C",64,45)
            self.display.textAligned(self.drawingTextLine2,"C",64,55)
        else:
            self.display.textAligned("not set stage","C",64,56)

##########  Ethernet
    def logicStageEthernet(self):
        if(self.bootStageChanged):
                self.drawingTextLine1="Ethernet module"
                self.drawingTextLine2="Init"
                self.tim = Timer(period=1000, mode=Timer.ONE_SHOT, callback=lambda t:self.initEthernet())
                self.bootStageChanged=False
        else:
            if self.isInitEthernet and self.needIPEthernet:
                if not self.ethernet.isConnected():
                    time.sleep_ms(10)
                else:
                    self.needIPEthernet=False
                    stats=self.ethernet.ifConfig()
                    self.logger.log(self.ethernet.ifConfig())
                    self.drawingTextLine2=stats[0]
                    self.tim = Timer(period=3000, mode=Timer.ONE_SHOT, callback=lambda t:self.stageChangerCallback(3))
            else:
                time.sleep_ms(1)

    def initEthernet(self):
        self.ethernet=Ethernet()
        self.ethernet.activate()
        self.nic=self.ethernet.getHandler()
        self.drawingTextLine2="Connecting"
        self.isInitEthernet=True

##########  FTP Updater
    def logicStageFTPUpdater(self):
        if(self.bootStageChanged):
                self.drawingTextLine1="FTP Updater"
                self.drawingTextLine2="Init"
                self.tim = Timer(period=1000, mode=Timer.ONE_SHOT, callback=lambda t:self.initFTPUpdater())
                self.bootStageChanged=False
        else:
            if self.isInitFTPUpdater and self.needDoneFTPUpdater:
                self.needIPEthernet=False
                stats=self.ethernet.ifConfig()
                self.logger.log(self.ethernet.ifConfig())
                self.drawingTextLine2=stats[0]
                self.tim = Timer(period=3000, mode=Timer.ONE_SHOT, callback=lambda t:self.stageChangerCallback(3))
            else:
                time.sleep_ms(1)

    def initFTPUpdater(self):
        self.isInitFTPUpdater=True

def threadRunnerFTPUpdate(log,nic):
    #if ConfigPico.ftpUpdate["ftpWork"]:
    logger=Debug()
    logger.enablePrintConsole=True
    logger.logText="ftpUpdateRunner"
    logger.warningText="ftpUpdateRunner"
    logger.errorText="ftpUpdateRunner"
    ftpUpdater = FTPUpdater(nic,logger)
    ftpUpdater.writeToPico=True
    ftpUpdater.writeToServer=False
    ftpUpdater.Update()