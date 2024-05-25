FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libevent-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

COPY . .

CMD python -u scripts/datagen/kafka_produce.py & python scripts/datagen/fetch_news.py
