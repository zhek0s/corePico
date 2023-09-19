import os
from core.date import Date

class Filesystem:
    allLocalfiles=list()
    allLocaldir=list()
    FILE_CODE = 0x8000
    
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
                    print("Created directory: "+createdPath)
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
        print("------------")
        print("LOCAL FILES")
        print("------------")
        for f in self.allLocalfiles:
            print(f)
        print("!!!dir!!!")
        for d in self.allLocaldir:
            print(d)
        print("---------")
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
                print(picoFile)
                self.allLocalfiles.append(picoFile)
            else:
                self.allLocaldir.append({"type":"d", "name":f, "path":dir})
                self.openLocalDir(dir+'/'+f)

    def isfile(self,path):
        stats=os.stat(path)
        return stats[0] == self.FILE_CODE, stats