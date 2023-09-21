"""Importing states for dict"""
from core.StateMachine.States.TestState import TestState
from core.StateMachine.States.BootState import BootState

class ConfigPico:
    """Class boot and init configs"""
    StateMachine={
        "startUpState":"BootState" # type: ignore
    }
    StateMachineStates={
        "TestState":TestState, # type: ignore
        "BootState":BootState # type: ignore
    }
    ftpUpdate={
        "ftpWork":True, # type: ignore
        "writeToServer":False, # type: ignore
        "writeToPico":False, # type: ignore
        "FTP_HOST":"192.168.0.120", # type: ignore
        "FTP_USER":"GILIJO", # type: ignore
        "FTP_PASS":"1", # type: ignore
        "FTP_PORT":21, # type: ignore
        "ignoreLocalFiles":list({"Files.txt",".gitignore",".micropico"}), # type: ignore
        "ignoreLocalDir":list({"temp"}), # type: ignore
        "ignoreFTPFiles":list({"Files.txt",".gitignore",".micropico"}), # type: ignore
        "ignoreFTPDir":list({"//temp","//utils","//.git","//.vscode"}), # type: ignore
        "UTCcorrection":3 # type: ignore
        }
    Network={
        "EthernetHostName":"EtherPico" # type: ignore
        }
    