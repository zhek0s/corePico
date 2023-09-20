from core.StateMachine.States.TestState import TestState
from core.StateMachine.States.BootState import BootState

class configPico:
    StateMachine={
        "startUpState":"TestState"
    }
    StateMachineStates={
        "TestState":TestState,
        "BootState":BootState
    }
    ftpUpdate={
        "ftpWork":True,    
        "writeToServer":False,
        "writeToPico":False,
        "FTP_HOST":"192.168.0.120",
        "FTP_USER":"GILIJO",
        "FTP_PASS":"1",
        "FTP_PORT":21,
        "ignoreLocalFiles":list({"Files.txt",".gitignore",".micropico"}),
        "ignoreLocalDir":list({"temp"}),
        "ignoreFTPFiles":list({"Files.txt",".gitignore",".micropico"}),
        "ignoreFTPDir":list({"//temp","//utils","//.git","//.vscode"}),
        "UTCcorrection":3
        }
    Network={
        "EthernetHostName":"EtherPico"
        }