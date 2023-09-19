import os
from core.date import Date

class Filesystem:
    allLocalfiles=list()
    allLocaldir=list()
    FILE_CODE = 0x8000
    logger=[]
    
    def __init__(self,debugLogger):
        self.logger=debugLogger    
    
    def openBinaryFile(self,fileName,arg):
        if(self.file_or_dir_exists(fileName)):
            return open(fileName,arg)
        else:
            path=list(fileName.split("/"))
            createdPath="/"
            for i in range(1,len(path)-1):
                createdPath+=path[i]
                if(not (self.file_or_dir_exists(createdPath))):
                    os.mkdir(createdPath)
                    self.logger.Log("Created directory: "+createdPath)
                createdPath+="/"
            f=open(fileName,"w")
            f.close()
            return open(fileName,arg)
    
    def file_or_dir_exists(self,filename):
        try:
            os.stat(filename)
            return True
        except OSError:
            return False
    
    def getLocalFilesystem(self):
        self.openLocalDir("/")
        self.logger.print("------------")
        self.logger.print("LOCAL FILES")
        self.logger.print("------------")
        for f in self.allLocalfiles:
            self.logger.print(f)
        self.logger.print("!!!dir!!!")
        for d in self.allLocaldir:
            self.logger.print(d)
        self.logger.print("---------")
        return self.allLocalfiles,self.allLocaldir

    def openLocalDir(self,dir):
        files = os.listdir(dir)
        for f in files:
            _isfile,stats=self.isfile(dir+'/'+f)
            if _isfile:
                timeDat=Date.unixTimeToHumanReadable(stats[8])
                picoFile={}
                picoFile["type"]="file"
                picoFile["name"]=f
                picoFile["path"]=dir
                picoFile.update(timeDat)
                self.logger.print(picoFile)
                self.allLocalfiles.append(picoFile)
            else:
                self.allLocaldir.append({"type":"d", "name":f, "path":dir})
                self.openLocalDir(dir+'/'+f)

    def isfile(self,path):
        stats=os.stat(path)
        return stats[0] == self.FILE_CODE, stats