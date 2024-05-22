python3 ./scripts/db/upload_schema.py;
sleep 60;
docker compose up -d --build;