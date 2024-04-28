python3 scripts/datagen.py | docker exec \
    -i kafka /opt/kafka/bin/kafka-console-producer.sh \
    --bootstrap-server localhost:9092 \
    --topic events;