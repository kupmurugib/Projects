from kafka import KafkaConsumer
import mysql.connector
import sys

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="admin",
  #database="acme"
  database="tripdata"
)

id_val = 1
#message_val = "dummystring2"
max_speed = 80

mycursor = mydb.cursor()
sql = "INSERT INTO trip (id, driver_id, driver_name, time_stamp, speed, truck_name, trip_id, route_number) VALUES (%s, %s,%s, %s, %s, %s, %s, %s)"
sql_exceed = "INSERT INTO overspeed (id, driver_id, driver_name, time_stamp, speed, truck_name, trip_id, route_number) VALUES (%s, %s,%s, %s, %s, %s, %s, %s)"

bootstrap_servers = ['localhost:9092']
topicName = 'tripData'
#consumer = KafkaConsumer (topicName, group_id = 'group1',bootstrap_servers = bootstrap_servers, auto_offset_reset = 'earliest')
consumer = KafkaConsumer (topicName, bootstrap_servers = bootstrap_servers)

try:
    for message in consumer:
        print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,message.offset, message.key,message.value))
        id_val = id_val + 1
        message_val = str(message.value)
        message_val = message_val.split('\'')[-2]
        driver_id, driver_name, time_stamp, speed, truck_name, trip_id, route_number = [msg.strip() for msg in message_val.split(',')]
        val = (id_val, driver_id, driver_name, time_stamp, speed, truck_name, trip_id, route_number)
        mycursor.execute(sql, val)
        mydb.commit()
        if int(speed) >= max_speed:
           mycursor.execute(sql_exceed, val)
           mydb.commit()
        print(mycursor.rowcount, "record inserted.")
except KeyboardInterrupt:
    sys.exit()


# In[ ]:




