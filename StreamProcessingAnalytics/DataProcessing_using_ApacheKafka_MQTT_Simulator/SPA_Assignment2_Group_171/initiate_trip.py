## Trip Data Simulator using the config json file
## Publishing the trip data to Mosquitto Broker
## Usage : initiate_trip.py <driver ID> < Vehicle Name> < Route Number>
## E.g., > initiate_trip.py 1 VHCL01 RT01

import sys
import os
import json
from datetime import datetime
import random
import time
import calendar

from random import randrange, uniform
import publish_data_to_mqtt_broker as mqttpub

mqttBrokerHost ="localhost"
topic_name = "VEHICLEDATA"

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

def get_geo_coordinates(route_number):
    with open("routes/"+route_number+".route", 'r')as rtfile:
        lines = rtfile.readlines()
        return lines[2:]

def generate_vehicle_speed(driver, driver_driving_pattern, truck_name, trip_id, route_number, coordinates):

    mqtt_client = mqttpub.initiate_mqtt_client(trip_id, mqttBrokerHost)
    min_speed = driver_driving_pattern['min-speed']
    max_speed = driver_driving_pattern['max-speed']
    for line in coordinates:
        lat, lon = (line.strip()).split()
        dateTimeObj = datetime.now()
        currnt_speed = random.randint(min_speed,max_speed)
        message_txt = str(driver['id']) + ", " + driver['name'] + ", " + str(dateTimeObj) + ", " +  str(currnt_speed) + ", " + str(truck_name) + ", " + str(trip_id) + ", " + str(route_number) + ", " + lat + ", " + lon
        mqttpub.send_message_to_mqtt_broker(mqtt_client, topic_name, message_txt)
        print(message_txt)
        time.sleep(300)


def initiate_trip(driver_id, truck_name, trip_id, route_number):
    driver = find_driver_details(driver_id, driver_info)
    if driver is None:
        print("Not able to find the driver details")
        return None
    driver_driving_pattern = get_driving_pattern_details(driver['pattern'], driver_pattern)
    coordinates = get_geo_coordinates(route_number)
    generate_vehicle_speed(driver, driver_driving_pattern, truck_name, trip_id, route_number, coordinates)


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