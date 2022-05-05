from pykafka import KafkaClient
import json

client = KafkaClient(hosts='127.0.0.1:9092')
for i in client.topics["bus_output_topic"].get_simple_consumer():
	x = i.value.decode()
	print('data:{0}\n'.format(i.value.decode()))
print("*************************************************")
	#try:
	#	final_dictionary = json.loads(x) 
	#	print(final_dictionary["key"] + "     " + final_dictionary["timestamp"])
	#except:
	#	print("")