docker run --rm -ti \
    --network=pinot \
    -v $(pwd):/tmp/pinot \
    --name pinot-batch-table-creation \
    apachepinot/pinot:latest AddTable \
    -schemaFile /tmp/pinot/schemas/companies_schema.json \
    -tableConfigFile /tmp/pinot/configs/companies_config.json \
    -controllerHost pinot-controller \
    -controllerPort 9000 -exec