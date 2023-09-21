# Driver code
if __name__ == "__main__":
    from machine import Pin, I2C, SPI
    import network
    import time
    from config import ConfigPico
    from core.FTPUpdater.FTPUpdater import FTPUpdater
    from core.Debug import Debug
    
    spi=SPI(0,2_000_000, mosi=Pin(19),miso=Pin(16),sck=Pin(18))
    nic = network.WIZNET5K(spi,Pin(17),Pin(20))
    print('Start')
    print('Getting ip')
    nic.active(True) 
    if ConfigPico.ftpUpdate["ftpWork"]:
        time.sleep(3)
        print(nic.ifconfig())
    logger=Debug()
    logger.enablePrintConsole=False
    logger.logText="forceUpdatePico"
    logger.warningText="forceUpdatePico"
    logger.errorText="forceUpdatePico"
    ftpUpdater = FTPUpdater(nic,logger)
    ftpUpdater.writeToServer=False
    ftpUpdater.forceUpdatePico=True
    ftpUpdater.Update()
