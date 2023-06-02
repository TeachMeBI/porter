from py2neo import *
from typing import List, Dict
import random
from datetime import datetime, timedelta
from config import *
from pprint import pprint


def random_time(start_time, end_time):
    start = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    end = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    delta = end - start
    random_second = random.randint(0, delta.total_seconds())
    result = start + timedelta(seconds=random_second)
    return result.strftime('%Y-%m-%d %H:%M:%S')


def get_user_hist_clicks(user_id: str) -> List[Dict[str, str | int]]:
    data: List[Dict[str, str | int]] = []
    hist_clicks = GRAPH.run(
        f"MATCH (il: ImpressionLog)-[h: HISTORY_CLICK]->(n: News) WHERE il.userId='{user_id}' RETURN h"
    ).data()
    for item in hist_clicks:
        try:
            data.append({
                'newsId': item['h'].nodes[1]['newsId'],
                'dwelltime': item['h']['dwelltime'],
                'exposureTime': item['h']['exposureTime']
            })
        except Exception as e:
            print(e)

    hist_clicks = GRAPH.run(
        f"MATCH (il: ImpressionLog)-[c: CLICKED]->(n: News) WHERE il.userId='{user_id}' RETURN c"
    ).data()
    for item in hist_clicks:
        try:
            start_time = item['c'].nodes[0]['start']
            end_time   = item['c'].nodes[0]['end']
            data.append({
                'newsId': item['c'].nodes[1]['newsId'],
                'dwelltime': item['c']['dwelltime'],
                'exposureTime': random_time(start_time, end_time)
            })
        except Exception as e:
            print(e)
    return data


if __name__ == '__main__':
    pprint(GRAPH.run(
        f"MATCH (n: News) WHERE n.newsId='N58104' return n"
    ).data()[0])