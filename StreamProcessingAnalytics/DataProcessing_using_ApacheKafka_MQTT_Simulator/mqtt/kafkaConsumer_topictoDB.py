from kafka import KafkaConsumer
import mysql.connector
import sys

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="admin",
  database="acme"
)

id_val = 40
message_val = "dummystring2"

mycursor = mydb.cursor()

sql = "INSERT INTO test (id, message) VALUES (%s, %s)"
#val = (1, "tripuser")
#val = (id_val, message_val)
'''
mycursor.execute(sql, val)
mydb.commit()
print(mycursor.rowcount, "record inserted.")

'''
bootstrap_servers = ['localhost:9092']
topicName = 'tripData'
#consumer = KafkaConsumer (topicName, group_id = 'group1',bootstrap_servers = bootstrap_servers, auto_offset_reset = 'earliest')
consumer = KafkaConsumer (topicName, bootstrap_servers = bootstrap_servers)

try:
    for message in consumer:
        print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,message.offset, message.key,message.value))
        id_val = id_val + 1
        message_val = str(message.value)
        val = (id_val, message_val)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
except KeyboardInterrupt:
    sys.exit()