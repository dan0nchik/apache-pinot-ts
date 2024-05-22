import json
import os

with open('config.json') as f:
    config = json.load(f)

for provider in config['providers']:
    tickers = config['providers'][provider]

    for ticker in tickers:
        
        config_template_file = f'configs/{provider}_config_template.json'
        schema_template_file = f'schemas/{provider}_schema_template.json'

    
        with open(config_template_file) as f:
            config_template_str = json.dumps(json.load(f))
            config_template_str = config_template_str.replace('TEMPLATE', ticker)
        
        with open(f'{ticker}_tmp_config.json', 'w+') as f:
            json.dump(json.loads(config_template_str), f)    


        with open(schema_template_file) as f:
            schema_template_str = json.dumps(json.load(f))
            schema_template_str = schema_template_str.replace('TEMPLATE', ticker)
        
        with open(f'{ticker}_tmp_schema.json', 'w+') as f:
            json.dump(json.loads(schema_template_str), f)  
            

        os.system(f"""docker run --rm -ti \
    --network=pinot\
    -v $(pwd):/tmp/pinot \
    --name pinot-batch-table-creation \
    apachepinot/pinot:latest AddTable \
    -schemaFile "/tmp/pinot/{ticker}_tmp_schema.json" \
    -tableConfigFile "/tmp/pinot/{ticker}_tmp_config.json" \
    -controllerHost pinot-controller \
    -controllerPort 9000 -exec""")
        
        os.remove(f'{ticker}_tmp_schema.json')
        os.remove(f'{ticker}_tmp_config.json')




