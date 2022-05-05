import json
from datetime import datetime
import random
import time

import paho.mqtt.client as mqtt 
from random import randrange, uniform
import time

#mqttBroker ="mqtt.eclipseprojects.io" 
mqttBroker ="localhost"

client = mqtt.Client("Temperature_Inside1")
client.connect(mqttBroker)

with open('config.json', 'r') as j:
    json_data = json.load(j)

driver_pattern = json_data['driver']['driving-patterns']
driver_info = json_data['driver']['special-drivers']

def find_driver_details(driver_id, driver_info):
    for driver in driver_info:
        if driver_id in driver.values():
            return driver
    return None

def get_driving_pattern_details(pattern_value, driver_pattern):
    for pattern in driver_pattern:
        if pattern_value in pattern.values():
            return pattern
    return None

def generate_vehicle_speed(driver, driver_driving_pattern):
    min_speed = driver_driving_pattern['min-speed']
    max_speed = driver_driving_pattern['max-speed']
    count = 0
    max_count = 50
    while (count <= max_count):
        count = count + 1
        dateTimeObj = datetime.now()
        currnt_speed = random.randint(min_speed,max_speed)
        client.publish("TEMPERATURE1", str(driver['id']) + " " + driver['name'] + " " + str(dateTimeObj) + " " +  str(currnt_speed))
        #client.publish("TEMPERATURE", currnt_speed)
        print(driver['id'], driver['name'], dateTimeObj, currnt_speed)
        time.sleep(1)


def initiate_trip(driver_id):
    driver = find_driver_details(driver_id, driver_info)
    if driver is None:
        print("Not ablet to find the driver details")
        return None
    driver_driving_pattern = get_driving_pattern_details(driver['pattern'], driver_pattern)
    generate_vehicle_speed(driver, driver_driving_pattern)


initiate_trip(1)
# initiate_trip(3)