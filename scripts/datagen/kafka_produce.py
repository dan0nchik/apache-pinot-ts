import asyncio
import configparser
import datetime
import json
from fetch_tinkoff import fetch_ticker
from aiokafka import AIOKafkaProducer
import logging

# Set up logging
logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Tickers configuration
with open('config.json') as f:
    config = json.load(f)
tickers = config['providers']['tinkoff']
print(tickers)
kafka_conf = {'bootstrap_servers': config['bootstrap_servers']}

async def produce_data():
    producer = AIOKafkaProducer(**kafka_conf)
    # Start the producer
    await producer.start()
    try:
        async def fetch_job(ticker: str):
            async for value in fetch_ticker(ticker):
                ts = int(datetime.datetime.now().timestamp() * 1000)
                symbol = ticker
                close = value[1]
                message = json.dumps({"ts": ts, "symbol": symbol, "price": close})
                try:
                    # Send message
                    await producer.send_and_wait(topic=ticker, value=message.encode('utf-8'))
                    logger.info(f"Message produced: {message}")
                except Exception as e:
                    logger.error(f"Failed to deliver message: {message}: {str(e)}")
        tasks = [fetch_job(ticker) for ticker in tickers]
        await asyncio.gather(*tasks)
    finally:
        # Ensure all messages are sent before closing
        await producer.stop()

asyncio.run(produce_data())
