import json
import os

with open("config.json") as f:
    config = json.load(f)


def replace_template(real_path, temp_path, ticker):
    with open(real_path) as f:
        template_str = json.dumps(json.load(f))
        template_str = template_str.replace("TEMPLATE", ticker)

    with open(temp_path, "w+") as f:
        json.dump(json.loads(template_str), f)


def save_and_upload(schema, config, ticker, offline: bool):

    if offline:
        tmp_schema_path = f"{ticker}_tmp_offline_schema.json"
        tmp_config_path = f"{ticker}_tmp_offline_config.json"
    else:
        tmp_schema_path = f"{ticker}_tmp_schema.json"
        tmp_config_path = f"{ticker}_tmp_config.json"

    replace_template(schema, tmp_schema_path, ticker)
    replace_template(config, tmp_config_path, ticker)

    os.system(
        f"""docker run --rm -ti \
                --network=pinot\
                -v $(pwd):/tmp/pinot \
                --name pinot-batch-table-creation \
                apachepinot/pinot:latest AddTable \
                -schemaFile "/tmp/pinot/{tmp_schema_path}" \
                -tableConfigFile "/tmp/pinot/{tmp_config_path}" \
                -controllerHost pinot-controller \
                -controllerPort 9000 -exec"""
    )

    os.remove(tmp_schema_path)
    os.remove(tmp_config_path)


for provider in config["providers"]:
    tickers = config["providers"][provider]["tickers"]

    for ticker in tickers:
        config_template_file = f"configs/{provider}_config_template.json"
        schema_template_file = f"schemas/{provider}_schema_template.json"
        if provider == "yahoo":
            offline_schema_template_file = (
                f"schemas/{provider}_offline_schema_template.json"
            )
            offline_config_template_file = (
                f"configs/{provider}_offline_config_template.json"
            )
            save_and_upload(
                offline_schema_template_file, offline_config_template_file, ticker, True
            )
        save_and_upload(schema_template_file, config_template_file, ticker, False)
