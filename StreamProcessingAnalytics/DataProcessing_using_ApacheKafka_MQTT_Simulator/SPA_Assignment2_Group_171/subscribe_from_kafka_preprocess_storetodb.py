## Code to consume the data from Kafka topic and pre-process them.
## Also, the raw_data and processed data are being written to database storage.

from kafka import KafkaConsumer
import mysql.connector
import sys

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="admin",
  database="tripdata"
)

id_val = 153
max_speed = 80

mycursor = mydb.cursor()
sql = "INSERT INTO trip (id, driver_id, driver_name, time_stamp, speed, truck_name, trip_id, route_number, latitude, longitude) VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s)"
sql_exceed = "INSERT INTO overspeed (id, driver_id, driver_name, time_stamp, speed, truck_name, trip_id, route_number, latitude, longitude) VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s)"

bootstrap_servers = ['localhost:9092']
topicName = 'tripData'
consumer = KafkaConsumer (topicName, bootstrap_servers = bootstrap_servers)

try:
    for message in consumer:
        print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,message.offset, message.key,message.value))
        id_val = id_val + 1
        message_val = str(message.value)
        message_val = message_val.split('\'')[-2]
        driver_id, driver_name, time_stamp, speed, truck_name, trip_id, route_number, latitude, longitude = [msg.strip() for msg in message_val.split(',')]
        val = (id_val, driver_id, driver_name, time_stamp, speed, truck_name, trip_id, route_number, latitude, longitude)
        mycursor.execute(sql, val)
        mydb.commit()
        if int(speed) >= max_speed:
           mycursor.execute(sql_exceed, val)
           mydb.commit()
        print(mycursor.rowcount, "record inserted.")
except KeyboardInterrupt:
    sys.exit()