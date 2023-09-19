from config import configPico
from core.date import Date
from core.Filesystem.Filesystem import Filesystem
from lib.ftp import FTP

CRLF = '\r\n'
class FTPUpdater:
    
    ftp=FTP()
    allfiles=list()
    alldir=list()
    filesystem = Filesystem()
    forceUpdatePico=False
    forceUpdateServer=False
    
    def __init__(self,nic):
        self.allfiles.clear()
        self.alldir.clear()
        FTP_HOST = configPico.ftpUpdate["FTP_HOST"]
        FTP_USER = configPico.ftpUpdate["FTP_USER"]
        FTP_PASS = configPico.ftpUpdate["FTP_PASS"]
        FTP_PORT = configPico.ftpUpdate["FTP_PORT"]   
        if configPico.ftpUpdate["ftpWork"]:
            self.ftp = FTP(FTP_HOST,FTP_PORT,FTP_USER,FTP_PASS,None,FTP.timeout,[nic.ifconfig()[0],""])
        else:
            print("FTPUpdater disabled in config.py!")
            
    def Update(self):
        self.getAllFiles()
        allLocalfiles,allLocaldir=self.filesystem.getLocalFilesystem()
        self.findDifferenceAndUpdate(self.allfiles,allLocalfiles,self.alldir,allLocaldir)
        self.ftp.quit()
        
    
    def getAllFiles(self):
        self.openDir("/")
        if len(self.alldir)!=0:
            for d in self.alldir:
                print("Opening: "+d["path"]+"/"+d["name"])
                self.ftp.cwd(d["path"]+"/"+d["name"])
                currDir=d["path"]+"/"+d["name"]
                self.openDir(currDir)
                self.ftp.cwd('..')

    def openDir(self,currDir):
        if(not(currDir in configPico.ftpUpdate["ignoreFTPDir"])):
            self.ftp.retrlines('MLSD',currDir,self.newLine)
            print("------------")
            print("FTP FILES")
            print("------------")
            for f in self.allfiles:
                print(f)
            print("!!!dir!!!")
            for d in self.alldir:
                print(d)
            print("---------")
        else:
            print("Ignoring path:"+currDir)

    def newLine(self,t,currDir):
        print(t)
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
        entry["hour"]=int(entry["modify"][8:10])+configPico.ftpUpdate["UTCcorrection"]
        entry["minute"]=entry["modify"][10:12]
        return entry
    
    def findDifferenceAndUpdate(self,fFtp,fLocal,dFtp,dLocal):
        print()
        print("Looking for difference...")
        filesFtp=list()
        filesLocal=list()
        for file in fFtp:
            for fileL in fLocal:
                if(file["name"]==fileL["name"]):
                    dat={"hour":file["hour"],"minute":file["minute"],"year":file["year"],"month":file["month"],"date":file["day"]}
                    datL={"hour":fileL["hour"],"minute":fileL["minute"],"year":fileL["year"],"month":fileL["month"],"date":fileL["day"]}
                    if(Date.biggerDate(dat,datL) or self.forceUpdatePico):
                        print("NEED UPDATE FILE:"+fileL["path"]+"/"+fileL["name"]+"   "+Date.niceDateFromDat(dat)+"  >>  "+Date.niceDateFromDat(datL))
                        if(not (file["name"] in configPico.ftpUpdate["ignoreFTPFiles"])):
                            if(configPico.ftpUpdate["writeToPico"]):
                                print("Download file: "+file["path"]+"/"+file["name"])
                                handle = self.filesystem.openBinaryFile(file["path"].rstrip("/") + "/" + file["name"].lstrip("/"), 'wb')
                                self.ftp.cwd(file["path"])
                                self.ftp.retrbinary('RETR %s' % file["name"], handle.write)
                            else:
                                print("Updating pico disable!")
                        else:
                            print("Ignore ftp file:"+file["name"])
                    else:
                        print("File no need update: "+fileL["path"]+"/"+fileL["name"]+"   "+Date.niceDateFromDat(dat)+"  <<  "+Date.niceDateFromDat(datL))
                    filesFtp.append(file["name"])
                    filesLocal.append(fileL["name"])
        for file in fFtp:
            if(not (file["name"] in filesFtp)):
                print("File found only on FTP: "+file["path"]+"/"+file["name"])
        for d in dLocal:
            find=False
            for dF in dFtp:
                if d["name"]==dF["name"] and d["path"]==dF["path"]:
                    find=True
            if (not (d["name"] in configPico.ftpUpdate["ignoreLocalDir"])) and (not find):
                print("Creating directory: "+d["path"]+"/"+d["name"])
                self.ftp.cwd(d["path"])
                self.ftp.mkd(d["name"])
                self.ftp.cwd("/")
        for file in fFtp:
            if((configPico.ftpUpdate["writeToPico"]) and (not (file["name"] in filesFtp))) or self.forceUpdatePico:
                if(not (file["name"] in configPico.ftpUpdate["ignoreFTPFiles"])):
                   print("Download file: "+file["path"]+"/"+file["name"])
                   handle = self.filesystem.openBinaryFile(file["path"].rstrip("/") + "/" + file["name"].lstrip("/"), 'wb')
                   self.ftp.cwd(file["path"])
                   self.ftp.retrbinary('RETR %s' % file["name"], handle.write)
                else:
                    print("Ignore ftp file:"+file["name"])

        for file in fLocal:
            if (not (file["name"] in filesLocal)) or self.forceUpdateServer:
                print("File found only on Pico: "+file["path"]+"/"+file["name"])
                if(configPico.ftpUpdate["writeToServer"] or self.forceUpdateServer):
                    if(not (file["name"] in configPico.ftpUpdate["ignoreLocalFiles"])):
                        f=self.filesystem.openBinaryFile(file["path"]+"/"+file["name"],'rb')
                        self.ftp.cwd(file["path"])
                        self.ftp.delete(file["name"])
                        self.ftp.storbinary("STOR "+file["name"], f)
                        f.close()
                    else:
                        print("Ignoring "+file["name"])
