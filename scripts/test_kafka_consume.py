from kafka import KafkaConsumer, KafkaProducer
import datetime
import uuid
import random
import json
import time


bootstrap_servers = ['localhost:9092']
topic = 'events'
consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers, value_deserializer=lambda x: json.loads(x))

for msg in consumer:
    print(msg.value)
    