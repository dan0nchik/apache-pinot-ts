import asyncio
import configparser
from datetime import datetime
import json
import fetch_tinkoff, fetch_yahoo
from aiokafka import AIOKafkaProducer
import logging

# Set up logging
logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Tickers configuration
with open("config.json") as f:
    config = json.load(f)
tickers_tinkoff = config["providers"]["tinkoff"]["tickers"]
tickers_yahoo = config["providers"]["yahoo"]["tickers"]
kafka_conf = {"bootstrap_servers": config["bootstrap_servers"]}


async def produce_data():
    producer = AIOKafkaProducer(**kafka_conf)
    # Start the producer
    await producer.start()
    try:

        async def fetch_job_tinkoff(ticker: str):
            async for value in fetch_tinkoff.fetch_ticker(ticker):
                symbol = ticker
                ts, open, high, low, close, volume = value
                message = json.dumps(
                    {
                        "ts": int(ts.timestamp() * 1000),
                        "ts_str": str(ts),
                        "symbol": symbol,
                        "open": open,
                        "high": high,
                        "low": low,
                        "close": close,
                        "volume": volume,
                    }
                )
                try:
                    # Send message
                    await producer.send_and_wait(
                        topic=ticker, value=message.encode("utf-8")
                    )
                    logger.info(f"Message produced: {message}")
                except Exception as e:
                    logger.error(f"Failed to deliver message: {message}: {str(e)}")

        async def fetch_job_yahoo(ticker: str):
            async for value in fetch_yahoo.fetch_ticker([ticker]):
                print(value)
                symbol, ts, price, change, day_volume = value
                message = json.dumps(
                    {
                        "ts": ts,
                        "ts_str": str(datetime.fromtimestamp(ts / 1e3)),
                        "symbol": symbol,
                        "price": price,
                        "change": change,
                        "day_volume": day_volume,
                    }
                )
                try:
                    # Send message
                    await producer.send_and_wait(
                        topic=ticker, value=message.encode("utf-8")
                    )
                    logger.info(f"Message produced: {message}")
                except Exception as e:
                    logger.error(f"Failed to deliver message: {message}: {str(e)}")

        tasks = [fetch_job_tinkoff(ticker) for ticker in tickers_tinkoff]
        # + [
        #    fetch_job_yahoo(ticker) for ticker in tickers_yahoo
        # ]
        await asyncio.gather(*tasks)
    finally:
        # Ensure all messages are sent before closing
        await producer.stop()


asyncio.run(produce_data())
