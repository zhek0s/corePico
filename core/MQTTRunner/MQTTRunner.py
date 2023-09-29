import time
from config import ConfigPico
from core.Debug import Debug
from core.MQTTRunner.MQTTClient import MQTTClient

class MQTTRunner:

    logger: Debug
    client: MQTTClient

    mqtt_server=""
    client_id=""
    port=0
    keepalive=0
    last_message = 0
    messageUpdateInterval = 500
    counter = 0

    topic_pub=""
    topic_sub=""
    callback=None

    def __init__(self,debugLogger):
        self.logger = debugLogger
        self.logger.print('Try to connect mqtt server')
        # #mqtt config
        self.mqtt_server = ConfigPico.MQTT["mqtt_server"]
        self.client_id=ConfigPico.MQTT["client_id"]
        self.topic_pub=ConfigPico.MQTT["topic_pub"]
        self.topic_sub=ConfigPico.MQTT["topic_sub"]
        self.port=ConfigPico.MQTT["port"]
        self.keepalive=ConfigPico.MQTT["keepalive"]
        try:
            self.client=self.mqtt_connect()
        except OSError as e:
            print(e)
            self.reconnect()
        self.last_message=time.ticks_ms()

    def mqtt_connect(self):
        client = MQTTClient(self.client_id, self.mqtt_server, self.port, keepalive=self.keepalive)
        client.set_callback(self.sub_cb)
        client.connect()
        self.logger.print('Connected to %s MQTT Broker'%(self.mqtt_server))
        return client

    # #reconnect & reset
    def reconnect(self):
        self.logger.print('Failed to connected to Broker. Reconnecting...')
        time.sleep(1)
        #machine.reset()

    def sub_cb(self, topic, msg):
        self.logger.print((topic.decode('utf-8'), msg.decode('utf-8')))
        if self.callback:
            self.callback(topic,msg)

    def diconnect(self):
        self.client.disconnect()

    def publish(self,data,topic_pub=None):
        if topic_pub:
            self.client.publish(topic_pub,data)
        else:
            self.client.publish(self.topic_pub,data)

    def subscribe(self,topic_sub=None,callback=None):
        if topic_sub:
            self.client.subscribe(topic_sub)
        else:
            self.client.subscribe(self.topic_sub)
        self.callback=callback
    
    def update(self):
        if(time.ticks_diff(time.ticks_ms(), self.last_message)>self.messageUpdateInterval):
            self.client.check_msg()
            self.last_message=time.ticks_ms()

# topic_msg = 'idk :('
# data={
#     'payload':{
#         'Temp':{
#             'val':'idk :('
#             },
#         'Hum':{
#             'val':'idk'
#             }
#     }
# }
# topic_sub = 'Temp'

# def main():
#     while True:
#         time.sleep(0.01)
#         temp,hum=th06.GetTempHum()
#         data['payload']['Temp']['val']=temp
#         data['payload']['Hum']['val']=hum
#         client.publish(topic_pub,json.dumps(data))
#         print('send')
#         time.sleep(1)
#         client.subscribe(topic_sub)
#         time.sleep(3)
    
#     client.disconnect()