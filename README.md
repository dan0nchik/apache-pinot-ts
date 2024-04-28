# Apache Pinot for Time Series

## Docs

https://docs.pinot.apache.org/

## Start cluster

``` 
docker compose up -d --build
```
## Structure (**DO NOT CHANGE FOLDER NAMES!**)

``` 
.
+-- configs
|   +-- Apache Pinot tables configs
|
+-- ingestion_configs
|   +-- Apache Pinot configs for data ingestion (offline tables)
|
+-- rawdata
|   +-- *csv files to load in tables (offline tables)
|
+-- schemas
|   +-- Apache Pinot schemas for tables
|
+-- scripts
|   +-- all necessary data processing scripts
|
+-- segments (in .gitignore)
|   +-- cached segments for offline tables
|
.
``` 
## Creating REALTIME table

1. Write schema + config (see docs)
2. Upload to Pinot with script
4. Test for ingesting: ```  python3 scripts/kafka_produce.py ``` 
4. If ok, restart in backgorund:   nohup python3 scripts/kafka_produce.py > ./kafka_ingest.log 2>&1 & ```

## Creating OFFLINE Table
1. Schema + config
2. Upload with script
3. Create segment config
4. Ingest data via batching with script

## Architecture

Data Stream -> Apache Kafka -> Apache Pinot

## Useful notes

Making file executable:
```
sudo chmod +x file_path
```

Making folder executable
```
sudo chmod -R +x directory_path
```

!!! careful with 
```
includeFileNamePattern: 'glob:**/*.csv'
```