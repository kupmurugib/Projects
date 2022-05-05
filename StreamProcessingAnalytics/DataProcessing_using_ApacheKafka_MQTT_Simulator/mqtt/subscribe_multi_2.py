# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 23:28:45 2021

@author: Kuprisayo
"""

import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, message):
    print("received message: " ,str(message.payload.decode("utf-8")))

#mqttBroker ="mqtt.eclipseprojects.io"
mqttBroker ="localhost"

topics = [("TEMPERATURE1",0),("TEMPERATURE2",0)]
client = mqtt.Client("Smartphone")
client.connect(mqttBroker) 
client.on_message=on_message
client.loop_start()

#client.subscribe("TEMPERATURE")
#client.subscribe("TEMPERATURE1",0)
#client.subscribe("TEMPERATURE2",0)
#client.subscribe([("TEMPERATURE2",0),("TEMPERATURE1",0)])
#client.subscribe("#",1)
#client.subscribe("#")
client.subscribe(topics)
#client.subscribe(["TEMPERATURE2", "TEMPERATURE1"],0)
#for t in topics:
    #client.subscribe(t)
    #client.on_message=on_message 

time.sleep(30)
#client.loop_stop()