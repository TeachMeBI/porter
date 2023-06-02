import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from typing import List, Dict


def fetch_mock_data(url: str, token: str, org: str, bucket: str, measurement: str, step: int) -> List[Dict[str, str | int]]:
    client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
    res: List[Dict[str, str | int]] = []
    query_api = client.query_api()
    query = f"""from(bucket: "{bucket}")
    |> range(start: -{step}m)
    |> filter(fn: (r) => r._measurement == "{measurement}")"""
    tables = query_api.query(query, org=org)
    for table in tables:
        for record in table:
            record_dict = record.values
            try:
                res.append({
                    'userId': record_dict['userId'],
                    'newsId': record_dict['newsId'],
                    'type':   record_dict['type'],
                    'exposureTime': record_dict['exposureTime'],
                    'dwelltime': int(record_dict['dwelltime']),
                })
            except Exception as e:
                print('Error:', e)
    return res


