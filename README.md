# Apache Pinot for Time Series

## Docs

https://docs.pinot.apache.org/

## Architecture

Data Stream -> Apache Kafka -> Apache Pinot

NOTE: server must have 16 GB of RAM!!!

## Starting cluster

``` 
docker compose up -d --build
```

## Creating REALTIME table with data streaming

1. Write schema + config (see docs) (Name files like: TABLENAME_schema.json and TABLENAME_config.json)
2. Upload to Pinot with script:
``` ./scripts/db/upload_schema.sh -n TABLENAME ``` 

## Creating OFFLINE Table
1. Write schema + config (see docs) (!! Name file like: TABLENAME_schema.json and TABLENAME_config.json)
2. Upload to Pinot with script:
``` ./scripts/db/upload_schema.sh -n TABLENAME ``` 
3. Create segment config
2. Upload and ingest to Pinot with script:
``` ./scripts/db/create_segment.sh -n TABLENAME ``` 

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