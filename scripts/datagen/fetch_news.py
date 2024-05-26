import json
import os
from traceback import print_tb
import feedparser
import schedule
import time

from fetch_utils import check_folders

with open("config.json") as f:
    config = json.load(f)
url = config["news"]["rss_feeds"][0]
interval = config["batch_ingest_interval"]


def save_news_entries(url):
    feed = feedparser.parse(url)
    news = []
    for entry in feed.entries:
        news.append(
            {
                "entry": {
                    "title": entry.get("title", "No Title"),
                    "link": entry.get("link", "No Link"),
                    "published": entry.get("published", "No Published Date"),
                    "summary": entry.get("summary", "No Summary"),
                }
            }
        )
    return news


def save_data_as_json(data, filename="./rawdata/news/news_data.json"):
    """Save the transformed data to a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def news_ingestion_job():
    check_folders("news")
    data = save_news_entries(url)
    save_data_as_json(data)
