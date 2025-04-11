"""Script to save OpenAPI in yaml"""

import requests
import yaml

if __name__ == '__main__':
    response = requests.get('http://localhost:8000/openapi.json')
    openapi_json = response.json()
    openapi_json['servers'] = [{'url': 'http://localhost:8000'}]

    with open('openapi.yaml', 'w', encoding='utf-8') as yaml_file:
        yaml.dump(openapi_json, yaml_file, sort_keys=False)
