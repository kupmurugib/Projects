## Send data from Mosquitto broker to Kafka topic.

import paho.mqtt.client as mqtt
import time

from kafka import KafkaProducer

bootstrap_servers = ['localhost:9092']
topicName = 'tripData'
producer = KafkaProducer(bootstrap_servers = bootstrap_servers)
producer = KafkaProducer()

def send_to_kafkatopic(topicName, message):
    ack = producer.send(topicName, message.encode('ascii'))
    metadata = ack.get()

def on_message(client, userdata, message):
    print("received message: " ,str(message.payload.decode("utf-8")))
    send_to_kafkatopic(topicName, str(message.payload.decode("utf-8")))

mqttBroker ="localhost"

topics = [("VEHICLEDATA",0)]
client = mqtt.Client("Smartphone")
client.connect(mqttBroker) 
client.on_message=on_message
client.loop_start()

client.subscribe(topics)

time.sleep(18000)