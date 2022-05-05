import sys
import os
import json
from datetime import datetime
import random
import time
import calendar

import paho.mqtt.client as mqtt 
from random import randrange, uniform
import time

#mqttBroker ="mqtt.eclipseprojects.io" 
mqttBroker ="localhost"

#client = mqtt.Client("Temperature_Inside1")
#client.connect(mqttBroker)

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

def generate_vehicle_speed(driver, driver_driving_pattern, truck_name, trip_id, route_number):

    client = mqtt.Client(trip_id)
    client.connect(mqttBroker, keepalive=300)
    min_speed = driver_driving_pattern['min-speed']
    max_speed = driver_driving_pattern['max-speed']
    count = 0
    max_count = 50
    while (count <= max_count):
        count = count + 1
        dateTimeObj = datetime.now()
        currnt_speed = random.randint(min_speed,max_speed)
        #client.publish("TEMPERATURE1", str(driver['id']) + " " + driver['name'] + " " + str(dateTimeObj) + " " +  str(currnt_speed))
        client.publish("VEHICLEDATA", str(driver['id']) + ", " + driver['name'] + ", " + str(dateTimeObj) + ", " +  str(currnt_speed) + ", " + str(truck_name) + ", " + str(trip_id) + ", " + str(route_number))
        #client.publish("TEMPERATURE", currnt_speed)
        print(driver['id'], driver['name'], dateTimeObj, currnt_speed)
        time.sleep(300)


def initiate_trip(driver_id, truck_name, trip_id, route_number):
    driver = find_driver_details(driver_id, driver_info)
    if driver is None:
        print("Not able to find the driver details")
        return None
    driver_driving_pattern = get_driving_pattern_details(driver['pattern'], driver_pattern)
    generate_vehicle_speed(driver, driver_driving_pattern, truck_name, trip_id, route_number)


if __name__ == '__main__':
    
    driver_id = 1
    truck_name = "TESLA"
    route_number = 'RT01'
    print(sys.argv[0])
    print(sys.argv[1:])
    driver_id = sys.argv[1]
    truck_name = sys.argv[2]
    route_number = sys.argv[3]
    trip_id = str(driver_id) + "_" + truck_name + "_" + str(route_number) + "_" + str(calendar.timegm(time.gmtime()))
    print(trip_id)
    initiate_trip(int(driver_id), truck_name, trip_id, route_number)
    # initiate_trip(3)