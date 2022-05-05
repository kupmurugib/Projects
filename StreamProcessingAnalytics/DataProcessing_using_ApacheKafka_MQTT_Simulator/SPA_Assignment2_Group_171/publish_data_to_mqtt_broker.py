## Code to publish the simulated data to Mosquitto broker.
## Imported in initiate_trip.py file

import paho.mqtt.client as mqtt

def initiate_mqtt_client(trip_id, mqttBrokerHost):
    client = mqtt.Client(trip_id)
    client.connect(mqttBrokerHost, keepalive=300)
    return client
def send_message_to_mqtt_broker(client, topic_name, message_txt):
    client.publish(topic_name,message_txt)