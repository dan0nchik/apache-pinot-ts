docker run --rm -ti \
    --network=apache-pinot-ts_default\
    -v ~/dev/apache-pinot-ts/:/tmp/pinot \
    --name pinot-batch-table-creation \
    apachepinot/pinot:latest AddTable \
    -schemaFile /tmp/pinot/schemas/schema-stream.json \
    -tableConfigFile /tmp/pinot/configs/table-config-stream.json \
    -controllerHost pinot-controller \
    -controllerPort 9000 -exec