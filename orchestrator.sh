GREEN='\033[0;32m'
NC='\033[0m' # No Color

docker compose up -d --build;
echo -e "${GREEN}Uploading DB schemas...${NC}";
python3 ./scripts/db/upload_schema.py;
echo -e "${GREEN}Creating news table...${NC}";
./scripts/db/upload_schema.sh -n news;
echo -e "${GREEN}Creating news table segment...${NC}";
./scripts/db/news_batch_ingest.sh;
echo -e "${GREEN}Creating offline tables segments...${NC}";
python3 -m pip install PyYAML
python3 ./scripts/db/yahoo_batch_ingest.py;
echo -e "${GREEN}Finished! Everything is up and running.${NC}";