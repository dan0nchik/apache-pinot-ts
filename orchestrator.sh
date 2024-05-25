GREEN='\033[0;32m'
NC='\033[0m' # No Color

docker compose up -d --build;
sleep 60;
echo -e "${GREEN}Uploading DB schemas...${NC}";
python3 ./scripts/db/upload_schema.py;
echo -e "${GREEN}Creating news table...${NC}";
./scripts/db/upload_schema.sh -n news;
echo -e "${GREEN}Creating news table segments...${NC}";
./scripts/db/batch_ingest.sh;
echo -e "${GREEN}Finished! Everything is up and running.${NC}";