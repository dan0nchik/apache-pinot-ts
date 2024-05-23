from ticker_pb2 import Ticker
import base64
import json
import websockets


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
