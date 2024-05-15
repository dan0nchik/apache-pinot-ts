import asyncio
import datetime
import uuid
import random
import json
import time
from fetch_tinkoff import TICKER, fetch_ticker
from confluent_kafka import Producer
import socket

conf = {'bootstrap.servers': 'kafka:9092'}
topic = 'events'
producer = Producer(conf)

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))

async def produce_data():
    async for value in fetch_ticker():
        ts = int(datetime.datetime.now().timestamp() * 1000)
        symbol = TICKER
        close = value[1]
        producer.produce(topic, json.dumps({"timestamp": ts, "symbol": symbol, "price": close}), callback=acked)
        producer.poll(1)

asyncio.run(produce_data())