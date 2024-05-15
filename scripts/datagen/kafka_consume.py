import json
from confluent_kafka import Consumer, KafkaError
from confluent_kafka import KafkaException

conf = {'bootstrap.servers': 'localhost:29092',
        'group.id': 'my_consumer_group',
        'auto.offset.reset': 'earliest'}

topic = 'events'

consumer = Consumer(conf)
consumer.subscribe([topic])

try:
    while True:
        msg = consumer.poll(timeout=1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event
                print('%% %s [%d] reached end at offset %d\n' %
                      (msg.topic(), msg.partition(), msg.offset()))
            elif msg.error():
                raise KafkaException(msg.error())
        else:
            # Message deserialization and processing
            try:
                data = json.loads(msg.value().decode('utf-8'))
                print("Received message: %s" % data)
                # Process the message here
            except Exception as e:
                print("Error processing message: %s" % str(e))

except KeyboardInterrupt:
    pass

finally:
    consumer.close()
