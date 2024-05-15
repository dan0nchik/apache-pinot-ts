while getopts n: flag
do
    case "${flag}" in
        n) table=${OPTARG};;
    esac
done

docker run --rm -ti \
    --network=pinot \
    -v $(pwd):/tmp/pinot \
    --name pinot-data-ingestion-job \
    apachepinot/pinot:latest LaunchDataIngestionJob \
    -jobSpecFile "/tmp/pinot/ingestion_configs/${table}_batch_job_spec.yml"