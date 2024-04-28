python3 scripts/datagen.py | docker exec \
    -i kafka /usr/bin/kafka-console-producer \
    --broker-list localhost:9092 \
    --topic events;
