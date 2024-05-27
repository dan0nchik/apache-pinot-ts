import asyncio
import datetime
import os
import json
import random
import time
from dotenv import load_dotenv

load_dotenv()

from tinkoff.invest import (
    AsyncClient,
    CandleInstrument,
    MarketDataRequest,
    SubscribeCandlesRequest,
    SubscriptionAction,
    SubscriptionInterval,
)
from fetch_utils import quotation_to_float, get_figi_by_ticker

TOKEN = os.environ["INVEST_TOKEN"]

with open("config.json") as f:
    config = json.load(f)
time_interval = config["providers"]["tinkoff"]["interval"]
if time_interval == "3m":
    sub = SubscriptionInterval.SUBSCRIPTION_INTERVAL_3_MIN
if time_interval == "1m":
    sub = SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_MINUTE
if time_interval == "5m":
    sub = SubscriptionInterval.SUBSCRIPTION_INTERVAL_FIVE_MINUTES
if time_interval == "15m":
    sub = SubscriptionInterval.SUBSCRIPTION_INTERVAL_FIFTEEN_MINUTES
if time_interval == "30m":
    sub = SubscriptionInterval.SUBSCRIPTION_INTERVAL_30_MIN
if time_interval == "1h":
    sub = SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_HOUR
if time_interval == "4h":
    sub = SubscriptionInterval.SUBSCRIPTION_INTERVAL_4_HOUR
if time_interval == "1d":
    sub = SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_DAY


async def fetch_ticker(TICKER: str):
    LOT, INSTRUMENT_ID = get_figi_by_ticker(TICKER)

    async def request_iterator():
        yield MarketDataRequest(
            subscribe_candles_request=SubscribeCandlesRequest(
                subscription_action=SubscriptionAction.SUBSCRIPTION_ACTION_SUBSCRIBE,
                instruments=[
                    CandleInstrument(
                        instrument_id=INSTRUMENT_ID,
                        interval=sub,
                    )
                ],
            )
        )
        while True:
            await asyncio.sleep(1)

    async with AsyncClient(TOKEN) as client:
        async for marketdata in client.market_data_stream.market_data_stream(
            request_iterator()
        ):
            if marketdata.candle is not None:
                yield (
                    marketdata.candle.time,
                    quotation_to_float(marketdata.candle.open),
                    quotation_to_float(marketdata.candle.high),
                    quotation_to_float(marketdata.candle.low),
                    quotation_to_float(marketdata.candle.close),
                    marketdata.candle.volume,
                )
