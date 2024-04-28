docker run --rm -ti \
    --network=apache-pinot-ts_default \
    -v ~/dev/apache-pinot-ts:/tmp/pinot \
    --name pinot-batch-table-creation \
    apachepinot/pinot:latest AddTable \
    -schemaFile /tmp/pinot/schemas/companies_schema.json \
    -tableConfigFile /tmp/pinot/configs/companies_config.json \
    -controllerHost pinot-controller \
    -controllerPort 9000 -exec