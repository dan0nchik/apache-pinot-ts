while getopts n: flag
do
    case "${flag}" in
        n) table=${OPTARG};;
    esac
done

docker run --rm -ti \
    --network=pinot\
    -v $(pwd):/tmp/pinot \
    --name pinot-batch-table-creation \
    apachepinot/pinot:latest AddTable \
    -schemaFile "/tmp/pinot/schemas/${table}_schema.json" \
    -tableConfigFile "/tmp/pinot/configs/${table}_config.json" \
    -controllerHost pinot-controller \
    -controllerPort 9000 -exec