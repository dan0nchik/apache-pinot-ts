docker run --rm -ti \
    --network=pinot \
    -v $(pwd):/tmp/pinot \
    --name pinot-data-ingestion-job \
    apachepinot/pinot:latest LaunchDataIngestionJob \
    -jobSpecFile /tmp/pinot/ingestion_configs/companies-batch-job-spec.yml