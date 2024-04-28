docker run --rm -ti \
    --network=apache-pinot-ts_default \
    -v ~/dev/apache-pinot-ts:/tmp/pinot \
    --name pinot-data-ingestion-job \
    apachepinot/pinot:latest LaunchDataIngestionJob \
    -jobSpecFile /tmp/pinot/segments/companies-batch-job-spec.yml