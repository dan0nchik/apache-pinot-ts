docker compose up -d --build;
sleep 60;
python3 ./scripts/db/upload_schema.py;