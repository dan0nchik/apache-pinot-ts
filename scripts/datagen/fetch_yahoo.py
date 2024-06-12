from ticker_pb2 import Ticker
import base64
import json
import websockets


import pandas as pd
import os
from yahoo_fin.stock_info import get_data
import pandas as pd
from datetime import datetime


with open("config.json") as f:
    config = json.load(f)
yahoo_tickers = config["providers"]["yahoo"]["tickers"]


def fetch_stock_data(ticker_name):
    now = datetime.now()
    today_date = now.strftime("%Y-%m-%d")
    base_dir = f"rawdata/yahoo_stocks/_BATCH_{ticker_name}"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    try:
        data = get_data(ticker_name)
        if data.empty:
            print(f"No data available for {ticker_name} on {today_date}")
            return

        file_path = os.path.join(base_dir, f"{ticker_name}.csv")
        data.reset_index(names=["ts"], inplace=True)
        data["ts"] = pd.to_datetime(data["ts"])
        data["ts"] = data["ts"].dt.strftime("%Y-%m-%d %H:%M:%S.%f")
        # data.drop(columns=["ts"], axis=1, inplace=True)
        data.to_csv(file_path, index=False)
    except Exception as e:
        print(f"Error fetching data for {ticker_name}: {e}")


def yahoo_ingestion_job():
    for ticker in yahoo_tickers:
        fetch_stock_data(ticker)


def deserialize(message):
    ticker_ = Ticker()
    message_bytes = base64.b64decode(message)
    ticker_.ParseFromString(message_bytes)
    return (ticker_.id, ticker_)


with open("config.json") as f:
    config = json.load(f)


async def fetch_ticker(worker_ticker: list):
    async with websockets.connect("wss://streamer.finance.yahoo.com/") as ws:
        await ws.send(json.dumps({"subscribe": worker_ticker}))
        while True:
            try:
                message = await ws.recv()
                result: Ticker = deserialize(message)[1]
                yield result.id, result.time, result.price, result.change, result.dayVolume
            except websockets.exceptions.ConnectionClosed:
                break
