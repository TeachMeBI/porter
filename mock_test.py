import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from config import *

mock_data = [
    'BILog,type="click",userId="U335175",newsId="N54028",exposureTime="2024-05-30\ 10:22:03",dwelltime=190 fieldKey="UNUSED"',
    'BILog,type="click",userId="U335175",newsId="N54647",exposureTime="2024-05-20\ 09:11:24",dwelltime=102 fieldKey="UNUSED"',
    'BILog,type="unclick",userId="U260848",newsId="N107780",exposureTime="2024-03-23\ 14:56:31",dwelltime=4 fieldKey="UNUSED"',
    'BILog,type="unclick",userId="U22232",newsId="N87169",exposureTime="2022-01-23\ 22:10:44",dwelltime=17 fieldKey="UNUSED"',
]

if __name__ == '__main__':
    client = influxdb_client.InfluxDBClient(url=URL, token=TOKEN, org=ORG)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(BUCKET, ORG, mock_data)

    query_api = client.query_api()

    query = f"""from(bucket: "{BUCKET}")
    |> range(start: -1m)
    |> filter(fn: (r) => r._measurement == "BILog")"""
    tables = query_api.query(query, org=ORG)\

    for table in tables:
        for record in table.records:
            print(record.values)