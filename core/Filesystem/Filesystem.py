import os
from core.date import Date

class Filesystem:
    allLocalfiles=list()
    allLocaldir=list()
    FILE_CODE = 0x8000

    def getLocalFilesystem(self):
        openLocalDir("/")
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
            _isfile,stats=isfile(dir+'/'+f)
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
                openLocalDir(dir+'/'+f)

    def isfile(self,path):
        stats=os.stat(path)
        return stats[0] == FILE_CODE, stats