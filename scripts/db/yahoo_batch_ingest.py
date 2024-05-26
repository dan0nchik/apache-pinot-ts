import json
import os
import yaml

with open("config.json") as f:
    config = json.load(f)


for provider in config["providers"]:
    tickers = config["providers"]["yahoo"]["tickers"]
    template_file_path = "ingestion_configs/yahoo_batch_job_spec.yml"
    for ticker in tickers:
        tmp_file_path = f"{ticker}_batch_job_spec.yml"
        with open(template_file_path) as f:
            list_doc = yaml.load(f, Loader=yaml.FullLoader)
            list_doc["inputDirURI"] = list_doc["inputDirURI"].replace(
                "TEMPLATE", ticker
            )
            list_doc["tableSpec"]["tableName"] = list_doc["tableSpec"][
                "tableName"
            ].replace("TEMPLATE", ticker)
        with open(tmp_file_path, "w") as f:
            yaml.dump(list_doc, f)
        os.system(
            f"""docker run --rm -ti \
                        --network pinot \
                        -v .:/tmp/pinot \
                        --name pinot-data-ingestion-job \
                        apachepinot/pinot:latest LaunchDataIngestionJob \
                        -jobSpecFile /tmp/pinot/{tmp_file_path}
        """
        )
        os.remove(tmp_file_path)
