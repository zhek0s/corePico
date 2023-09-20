
class Debug:
    
    printCallback=[]
    logCallback=[]
    warningCallback=[]
    errorCallback=[]
    enablePrintConsole=True
    printText=""
    logText=""
    warningText=""
    errorText=""
    
    
    def print(self,text):
        if(self.enablePrintConsole):
            if(self.printText!=""):
                print(self.printText)
            print(text)
        for callback in self.printCallback:
            callback(self.printText,text)
    
    def log(self,text):
        print()
        print(self.logText+" LOG:")
        print(text)
        for callback in self.logCallback:
            callback(self.logText,text)
        
    def warning(self,text):
        print()
        print(self.warningText+" WARNING:")
        print(text)
        for callback in self.warningCallback:
            callback(self.warningText,text)
        
    def error(self,text):
        print()
        print(self.errorText+" ERROR:")
        print(text)
        for callback in self.errorCallback:
            callback(self.errorText,text)
        
    def addPrintCallback(self,func):
        self.printCallback.append(func)
        
    def addLogCallback(self,func):
        self.logCallback.append(func)
        
    def addWarningCallback(self,func):
        self.warningCallback.append(func)
        
    def addErrorCallback(self,func):
        self.errorCallback.append(func)
        
    def removePrintCallback(self,func):
        self.printCallback.append(func)
        
    def removeLogCallback(self,func):
        self.logCallback.remove(func)
        
    def removeWarningCallback(self,func):
        self.warningCallback.remove(func)
        
    def removeErrorCallback(self,func):
        self.errorCallback.remove(func)
