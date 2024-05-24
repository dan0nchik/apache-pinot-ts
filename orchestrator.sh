docker compose up -d --build;
sleep 60;
# python3 ./scripts/db/upload_schema.py;
./scripts/db/upload_schema.sh -n news;
./scripts/db/batch_ingest.sh;