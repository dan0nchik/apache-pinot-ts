import asyncio
import os
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
TICKER="SBER"
LOT, INSTRUMENT_ID = get_figi_by_ticker(TICKER)
print(LOT, INSTRUMENT_ID)

async def fetch_ticker():
    async def request_iterator():
        yield MarketDataRequest(
            subscribe_candles_request=SubscribeCandlesRequest(
                subscription_action=SubscriptionAction.SUBSCRIPTION_ACTION_SUBSCRIBE,
                instruments=[
                    CandleInstrument(
                        instrument_id=INSTRUMENT_ID,
                        interval=SubscriptionInterval.SUBSCRIPTION_INTERVAL_3_MIN,
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
                yield (marketdata.candle.volume, quotation_to_float(marketdata.candle.close))