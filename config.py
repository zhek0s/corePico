class ConfigPico:
    """Class boot and init configs"""
    StateMachine={
        "startUpState":"BootState" # type: ignore
    }
    ftpUpdate={
        "ftpWork":False, # type: ignore
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
    MQTT={
        "mqttWork":True, # type: ignore
        "mqtt_server":'192.168.0.120', # type: ignore
        "port":1883, # type: ignore
        "keepalive":60, # type: ignore
        "client_id":'pico_with_temp', # type: ignore
        "topic_pub":'mainController', # type: ignore
        "topic_sub":'mainController' # type: ignore
    }