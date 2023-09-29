from config import ConfigPico
from core.date import Date
from core.Debug import Debug
from core.Filesystem.Filesystem import Filesystem
from lib.ftp import FTP

CRLF = '\r\n'
class FTPUpdater:
    
    ftp: FTP
    allfiles=list()
    alldir=list()
    filesystem: Filesystem
    forceUpdatePico=False
    forceUpdateServer=False
    writeToPico=True
    writeToServer=False
    logger: Debug
    
    def __init__(self,nic,debugLogger):
        self.logger=debugLogger
        self.filesystem=Filesystem(debugLogger)
        self.allfiles.clear()
        self.alldir.clear()
        
        self.writeToPico=ConfigPico.ftpUpdate["writeToPico"]
        self.writeToServer=ConfigPico.ftpUpdate["writeToServer"]
        FTP_HOST = ConfigPico.ftpUpdate["FTP_HOST"]
        FTP_USER = ConfigPico.ftpUpdate["FTP_USER"]
        FTP_PASS = ConfigPico.ftpUpdate["FTP_PASS"]
        FTP_PORT = ConfigPico.ftpUpdate["FTP_PORT"]   
        if ConfigPico.ftpUpdate["ftpWork"]:
            self.ftp = FTP(self.logger,FTP_HOST,FTP_PORT,FTP_USER,FTP_PASS,None,FTP.timeout,[nic.ifconfig()[0],""])
        else:
            self.logger.warning("FTPUpdater disabled in config.py!")
            
    def Update(self):
        self.logger.log("Reading files on server")
        self.getAllFiles()
        self.logger.log("Reading files on pico")
        allLocalfiles,allLocaldir=self.filesystem.getLocalFilesystem()
        self.logger.log("Finding difference and update")
        self.findDifferenceAndUpdate(self.allfiles,allLocalfiles,self.alldir,allLocaldir)
        self.logger.log("FTPUpdater work done.")
        self.ftp.quit()
        
    
    def getAllFiles(self):
        self.openDir("/")
        if len(self.alldir)!=0:
            for d in self.alldir:
                self.logger.print("Opening: "+d["path"]+"/"+d["name"])
                self.ftp.cwd(d["path"]+"/"+d["name"])
                currDir=d["path"]+"/"+d["name"]
                self.openDir(currDir)
                self.ftp.cwd('..')

    def openDir(self,currDir):
        if(not(currDir in ConfigPico.ftpUpdate["ignoreFTPDir"])):
            self.ftp.retrlines('MLSD',currDir,self.newLine)
            self.logger.print("------------")
            self.logger.print("FTP FILES")
            self.logger.print("------------")
            for f in self.allfiles:
                self.logger.print(f)
            self.logger.print("!!!dir!!!")
            for d in self.alldir:
                self.logger.print(d)
            self.logger.print("---------")
        else:
            self.logger.print("Ignoring path:"+currDir)

    def newLine(self,t,currDir):
        self.logger.print(t)
        line=self.handleFTPlistResp(t,currDir)
        if(line["type"]=="file"):
            self.allfiles.append(line)
        else:
            self.alldir.append(line)

    def handleFTPlistResp(self,obj,currDir):
        facts_found, _, name = obj.rstrip(CRLF).partition(' ')
        entry = {}
        for fact in facts_found[:-1].split(";"):
            key, _, value = fact.partition("=")
            entry[key.lower()] = value
        entry["name"]=name
        entry["path"]=currDir
        entry["year"]=entry["modify"][0:4]
        entry["month"]=entry["modify"][4:6]
        entry["day"]=entry["modify"][6:8]
        entry["hour"]=int(entry["modify"][8:10])+ConfigPico.ftpUpdate["UTCcorrection"]
        if(int(entry["hour"])>23):
            entry["hour"]-=24
            entry["day"]=int(entry["day"])+1
        entry["minute"]=entry["modify"][10:12]
        return entry
    
    def findDifferenceAndUpdate(self,fFtp,fLocal,dFtp,dLocal):
        self.logger.print("")
        self.logger.print("Looking for difference...")
        filesFtp=list()
        filesLocal=list()
        for file in fFtp:
            for fileL in fLocal:
                if(file["name"]==fileL["name"]):
                    filesFtp.append(file["name"])
                    filesLocal.append(fileL["name"])
                    dat={"hour":file["hour"],"minute":file["minute"],"year":file["year"],"month":file["month"],"date":file["day"]} # type: ignore
                    datL={"hour":fileL["hour"],"minute":fileL["minute"],"year":fileL["year"],"month":fileL["month"],"date":fileL["day"]} # type: ignore
                    if(Date.biggerDate(dat,datL) or self.forceUpdatePico): # type: ignore
                        self.logger.log("NEED UPDATE FILE:"+fileL["path"]+"/"+fileL["name"]+"   "+Date.niceDateFromDat(dat)+"  >>  "+Date.niceDateFromDat(datL)) # type: ignore
                        if(not (file["name"] in ConfigPico.ftpUpdate["ignoreFTPFiles"])):
                            if(self.writeToPico):
                                self.logger.log("Download file: "+file["path"]+"/"+file["name"])
                                handle = self.filesystem.openBinaryFile(file["path"].rstrip("/") + "/" + file["name"].lstrip("/"), 'wb')
                                self.ftp.cwd(file["path"])
                                self.ftp.retrbinary('RETR %s' % file["name"], handle.write)
                                handle.close()
                            else:
                                self.logger.warning("Updating pico disable!")
                        else:
                            self.logger.log("Ignore ftp file:"+file["name"])
                    else:
                        self.logger.log("File no need update: "+fileL["path"]+"/"+fileL["name"]+"   "+Date.niceDateFromDat(dat)+"  <<  "+Date.niceDateFromDat(datL)) # type: ignore
                        filesLocal.remove(file["name"])
                    
        for file in fFtp:
            if(not (file["name"] in filesFtp)):
                self.logger.print("File found only on FTP: "+file["path"]+"/"+file["name"])
        for d in dLocal:
            find=False
            for dF in dFtp:
                if d["name"]==dF["name"] and d["path"]==dF["path"]:
                    find=True
            if (not (d["name"] in ConfigPico.ftpUpdate["ignoreLocalDir"])) and (not find):
                self.logger.log("Creating directory: "+d["path"]+"/"+d["name"])
                self.ftp.cwd(d["path"])
                self.ftp.mkd(d["name"])
                self.ftp.cwd("/")
        for file in fFtp:
            if((self.writeToPico) and (not (file["name"] in filesFtp))) or self.forceUpdatePico:
                if(not (file["name"] in ConfigPico.ftpUpdate["ignoreFTPFiles"])):
                    self.logger.log("Download file: "+file["path"]+"/"+file["name"])
                    handle = self.filesystem.openBinaryFile(file["path"].rstrip("/") + "/" + file["name"].lstrip("/"), 'wb')
                    self.ftp.cwd(file["path"])
                    self.ftp.retrbinary('RETR %s' % file["name"], handle.write)
                else:
                    self.logger.log("Ignore ftp file:"+file["name"])

        for file in fLocal:
            if (not (file["name"] in filesLocal)) or self.forceUpdateServer:
                self.logger.print("File found only on Pico or need update on server: "+file["path"]+"/"+file["name"])
                if(self.writeToServer or self.forceUpdateServer):
                    if(not (file["name"] in ConfigPico.ftpUpdate["ignoreLocalFiles"])):
                        self.logger.log("Upload file to Server: "+file["path"]+"/"+file["name"])
                        f=self.filesystem.openBinaryFile(file["path"]+"/"+file["name"],'rb')
                        self.ftp.cwd(file["path"])
                        self.ftp.delete(file["name"])
                        self.ftp.storbinary("STOR "+file["name"], f)
                        f.close()
                    else:
                        self.logger.log("Ignoring "+file["name"])
