docker run --rm -ti \
            --network pinot \
            -v .:/tmp/pinot \
            --name pinot-data-ingestion-job \
            apachepinot/pinot:latest LaunchDataIngestionJob \
             -jobSpecFile /tmp/pinot/ingestion_configs/news_batch_job_spec.yml
