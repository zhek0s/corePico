import time
import framebuf
from machine import Timer
from config import ConfigPico
from core.Debug import Debug
from core.FTPUpdater.FTPUpdater import FTPUpdater
from core.MQTTRunner.MQTTRunner import MQTTRunner
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

    ftpUpdater: FTPUpdater
    isInitFTPUpdater=False
    needDoneFTPUpdater=ConfigPico.ftpUpdate["ftpWork"]
    logFTPUpdater=["Started"]
    ftpUpdaterStage=0

    mqtt: MQTTRunner
    needConnectMQTT=ConfigPico.MQTT["mqttWork"]
    isInitMQTT=False

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
        elif self.bootStage==4:
            self.logicStageMQTTInit()
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
        elif self.bootStage==3:
            self.display.textAligned(self.drawingTextLine1,"C",64,45)
            self.display.textAligned(self.logFTPUpdater[-1],"C",64,55)
        elif self.bootStage==4:
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
                self.logFTPUpdater.append("Init")
                if self.needDoneFTPUpdater:
                    self.tim = Timer(period=1000, mode=Timer.ONE_SHOT, callback=lambda t:self.initFTPUpdater())
                else:
                    self.tim = Timer(period=2000, mode=Timer.ONE_SHOT, callback=lambda t:self.stageChangerCallback(4))
                    self.logFTPUpdater.append("Aborted")
                self.bootStageChanged=False
        else:
            if self.isInitFTPUpdater and self.needDoneFTPUpdater:
                self.threadRunnerFTPUpdate()
                time.sleep_ms(1)
            else:
                time.sleep_ms(1)

    def initFTPUpdater(self):
        self.isInitFTPUpdater=True
        logger=Debug()
        logger.enablePrintConsole=False
        logger.logText="ftpUpdateRunner"
        logger.warningText="ftpUpdateRunner"
        logger.errorText="ftpUpdateRunner"
        self.ftpUpdater = FTPUpdater(self.nic,logger)
        self.ftpUpdater.writeToPico=True
        self.ftpUpdater.writeToServer=False
        self.ftpUpdaterStage=1

    def threadRunnerFTPUpdate(self):
        if self.ftpUpdaterStage==1:
            self.ftpUpdater.logger.log("Reading files on server")
            self.logFTPUpdater.append("Reading Server")
            self.Draw()
            self.ftpUpdater.getAllFiles()
        elif self.ftpUpdaterStage==2:
            self.ftpUpdater.logger.log("Reading files on pico")
            self.logFTPUpdater.append("Reading Pico")
            self.Draw()
            self.allLocalfiles,self.allLocaldir=self.ftpUpdater.filesystem.getLocalFilesystem()
        elif self.ftpUpdaterStage==3:
            self.ftpUpdater.logger.log("Finding difference and update")
            self.logFTPUpdater.append("Updating...")
            self.Draw()
            self.ftpUpdater.findDifferenceAndUpdate(self.ftpUpdater.allfiles,self.allLocalfiles,self.ftpUpdater.alldir,self.allLocaldir)
        elif self.ftpUpdaterStage==4:
            self.ftpUpdater.logger.log("FTPUpdater work done.")
            self.logFTPUpdater.append("Done")
            self.Draw()
            self.ftpUpdater.ftp.quit()
            self.ftpUpdater=[] # type: ignore
            self.tim = Timer(period=3000, mode=Timer.ONE_SHOT, callback=lambda t:self.stageChangerCallback(4))
        self.ftpUpdaterStage+=1

##########  MQTT Init
    def logicStageMQTTInit(self):
        if(self.bootStageChanged):
                self.drawingTextLine1="MQTT"
                self.drawingTextLine2="Init"
                if self.needConnectMQTT:
                    self.tim = Timer(period=1000, mode=Timer.ONE_SHOT, callback=lambda t:self.initMQTT())
                else:
                    self.tim = Timer(period=2000, mode=Timer.ONE_SHOT, callback=lambda t:self.stageChangerCallback(5))
                    self.drawingTextLine2="Aborted"
                self.bootStageChanged=False
        else:
            if self.isInitMQTT and self.needConnectMQTT:
                self.mqtt.update()
                time.sleep_ms(10)
            else:
                time.sleep_ms(1)

    def initMQTT(self):
        self.isInitMQTT=True
        logger=Debug()
        logger.enablePrintConsole=True
        logger.logText="MQTTRunner"
        logger.warningText="MQTTRunner"
        logger.errorText="MQTTRunner"
        self.mqtt = MQTTRunner(logger)
        self.mqtt.publish("Booted")
        self.mqtt.subscribe()
        #######TODO add information about boot
