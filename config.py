from py2neo import *
import json

with open('config.json', 'r', encoding='utf-8') as f:
    configs = json.load(f)

# neo4j
GRAPH = Graph(
    configs['neo_url'], 
    auth=(configs['neo_usr'], configs['neo_password']), 
    name=configs['neo_name']
)

# influxdb params
TOKEN  = configs['influx_token']   # test
URL    = configs['influx_url']     # test
ORG    = configs['org']
BUCKET = configs['bucket']
MEASUREMENT = configs['measurement']

INTERVAL = configs['interval']          # measuring in minute

if __name__ == '__main__':
    print(configs)