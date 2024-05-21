import asyncio
import datetime
import json
from fetch_tinkoff import TICKER, fetch_ticker
from aiokafka import AIOKafkaProducer
import logging

# Set up logging
logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Kafka configuration
conf = {
    'bootstrap_servers': 'kafka:9092'
}
topic = 'events'

async def produce_data():
    producer = AIOKafkaProducer(**conf)

    # Start the producer
    await producer.start()
    try:
        async for value in fetch_ticker():
            ts = int(datetime.datetime.now().timestamp() * 1000)
            symbol = TICKER
            close = value[1]
            message = json.dumps({"ts": ts, "symbol": symbol, "price": close})
            try:
                # Send message
                await producer.send_and_wait(topic, message.encode('utf-8'))
                logger.info(f"Message produced: {message}")
            except Exception as e:
                logger.error(f"Failed to deliver message: {message}: {str(e)}")
    finally:
        # Ensure all messages are sent before closing
        await producer.stop()

async def main():
    await produce_data()

asyncio.run(main())
