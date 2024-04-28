import datetime
import uuid
import random
import json
import time

from confluent_kafka import Producer
import socket

conf = {'bootstrap.servers': 'localhost:29092'}
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
    time.sleep(10)
    producer.produce(topic, json.dumps({"ts": ts, "uuid": id, "count": count}), callback=acked)
    producer.poll(1)