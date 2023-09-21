# print('Try to connect mqtt server')

# #mqtt config
# mqtt_server = '192.168.0.120'
# client_id = 'pico_with_temp'
# topic_pub = 'mainController'
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

# last_message = 0
# message_interval = 5
# counter = 0

# def mqtt_connect():
#     client = MQTTClient(client_id, mqtt_server, 3000, keepalive=60)
#     client.set_callback(sub_cb)
#     client.connect()
#     print('Connected to %s MQTT Broker'%(mqtt_server))
#     return client

# #reconnect & reset
# def reconnect():
#     print('Failed to connected to Broker. Reconnecting...')
#     time.sleep(5)
#     machine.reset()

# def sub_cb(topic, msg):
#     print((topic.decode('utf-8'), msg.decode('utf-8')))
    
# def main():
#     try:
#         client=mqtt_connect()
#     except OSError as e:
#         reconnect()
    
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