class configPico:
    ftpUpdate={
        "ftpWork":True,    
        "writeToServer":False,
        "writeToPico":False,
        "FTP_HOST":"192.168.0.120",
        "FTP_USER":"GILIJO",
        "FTP_PASS":"1",
        "FTP_PORT":21,
        "ignoreLocalFiles":list({"Files.txt"}),
        "ignoreLocalDir":list({"temp"}),
        "ignoreFTPFiles":list({"Files.txt"}),
        "ignoreFTPDir":list({"//temp","//utils","//.git"}),
        "UTCcorrection":3
        }
    Network={
        "EthernetHostName":"EtherPico"
        }