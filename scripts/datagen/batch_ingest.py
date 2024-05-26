import json
import time
from fetch_news import news_ingestion_job
from fetch_yahoo import yahoo_ingestion_job
import schedule

with open("config.json") as f:
    config = json.load(f)
interval = config["batch_ingest_interval"]
schedule.every(interval).minutes.do(news_ingestion_job)
schedule.every(interval).minutes.do(yahoo_ingestion_job)

news_ingestion_job()
yahoo_ingestion_job()

while True:
    schedule.run_pending()
    time.sleep(1)
