import time
import datetime
import schedule
from py2neo import *
from fetch_influx import fetch_mock_data
from make_log import make_log
from config import *


def task():
    
    def n_min_before_now(n: int) -> str:
        now = datetime.datetime.now()
        before = now - datetime.timedelta(minutes=n)
        return before.strftime('%Y-%m-%d %H:%M:%S')
    
    now = n_min_before_now(0)
    before = n_min_before_now(10)
    mock = fetch_mock_data(URL, TOKEN, ORG, BUCKET, MEASUREMENT, INTERVAL)
    if len(mock) == 0:
        print('No mock data found.')
        return
    user_clicks, user_unclicks, user_histclicks, user_ids = make_log(mock)
    try:
        for user_id in user_ids:
            impression_log = Node("ImpressionLog", userId=user_id, start=before, end=now)
            GRAPH.create(impression_log)
            try:
                if user_id in user_clicks:
                    for news_id, _, dwelltime in user_clicks[user_id]:
                        news = GRAPH.run(
                            f"MATCH (n: News) WHERE n.newsId='{news_id}' return n"
                        ).data()[0]['n']
                        clicked = Relationship(impression_log, "CLICKED", news, dwelltime=dwelltime)
                        GRAPH.create(clicked)
            except Exception as e:
                print(f'click relationship insert failed: {e.with_traceback()}')
            
            try:
                if user_id in user_unclicks:
                    for news_id, _, _ in user_unclicks[user_id]:
                        news = GRAPH.run(
                            f"MATCH (n: News) WHERE n.newsId='{news_id}' return n"
                        ).data()[0]['n']
                        unclicked = Relationship(impression_log, "UNCLICKED", news)
                        GRAPH.create(unclicked)
            except Exception as e:
                print(f'unclick relationship insert failed: {e.with_traceback()}')
            
            try:
                if user_id in user_histclicks:
                    for news_id, exposureTime, dwelltime in user_histclicks[user_id]:
                        news = GRAPH.run(
                            f"MATCH (n: News) WHERE n.newsId='{news_id}' return n"
                        ).data()[0]['n']
                        hist_click = Relationship(impression_log, "HISTORY_CLICK", news, exposureTime=exposureTime, dwelltime=dwelltime)
                        GRAPH.create(hist_click)
            except Exception as e:
                print(f'histclick relationship insert failed: {e.with_traceback()}')

    except Exception as e:
        print(f'Exception: {e.with_traceback()}')


schedule.every(INTERVAL).minutes.do(task)


if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
    # task()