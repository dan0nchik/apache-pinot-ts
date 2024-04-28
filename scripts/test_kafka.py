from kafka import KafkaConsumer, KafkaProducer
import datetime
import uuid
import random
import json
import time


from confluent_kafka import Producer
import socket

conf = {'bootstrap.servers': 'localhost:9092'}
topic = 'events'
producer = Producer(conf)

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))
while True:
    ts = int(datetime.datetime.now().timestamp() * 1000)
    id = str(uuid.uuid4())
    count = random.randint(0, 1000)
    
    producer.produce(topic, json.dumps({"ts": ts, "uuid": id, "count": count}), callback=acked)
    producer.poll(1)


# bootstrap_servers = 'localhost:9092'

# producer = KafkaProducer(bootstrap_servers=bootstrap_servers, acks='all', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
