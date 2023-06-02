from typing import List, Dict, Set, Tuple
from fetch_neo import get_user_hist_clicks
from pprint import pprint

def get_str_processed(s: str) -> str:
    if not isinstance(s, str):
        return ''
    return s.strip('"')

def make_log(mock: List[Dict[str, str | int]]):
    '''
    mock: [{
        'userId': record_dict['userId'],
        'newsId': record_dict['newsId'],
        'type':   record_dict['type'],
        'exposureTime': record_dict['exposureTime'],
        'dwelltime': int(record_dict['dwellTime']),
    }]
    '''
    if len(mock) == 0:
        return None

    user_clicks: Dict[str, List[Tuple[str, str, int]]] = {}
    user_unclicks: Dict[str, List[Tuple[str, str, int]]] = {}
    user_histclicks: Dict[str, List[Tuple[str, str, int]]] = {}
    userIds: Set[str] = set()

    for m in mock:
        try:
            userIds.add(get_str_processed(m['userId']))
        except Exception as e:
            print(e)

    for m in mock:
        try:
            userId, newsId = get_str_processed(m['userId']), get_str_processed(m['newsId'])
            exposureTime, dwelltime = get_str_processed(m['exposureTime']), int(m['dwelltime'])
            if get_str_processed(m['type']) == 'click':
                if userId in user_clicks:
                    user_clicks[userId].append((newsId, exposureTime, dwelltime))
                else:
                    user_clicks[userId] = [(newsId, exposureTime, dwelltime)]
            
            elif get_str_processed(m['type']) == 'unclick':
                if userId in user_unclicks:
                    user_unclicks[userId].append((newsId, exposureTime, dwelltime))
                else:
                    user_unclicks[userId] = [(newsId, exposureTime, dwelltime)]
        except Exception as e:
            print(e.with_traceback())

    for userId in userIds:
        try:
            hist = get_user_hist_clicks(userId)
            if len(hist) == 0:
                continue
            if userId in user_histclicks:
                user_histclicks[userId] += [(t['newsId'], t['exposureTime'], t['dwelltime']) for t in hist]
            else:
                user_histclicks[userId] = [(t['newsId'], t['exposureTime'], t['dwelltime']) for t in hist]
        except Exception as e:
            print(e.with_traceback())

    return user_clicks, user_unclicks, user_histclicks, userIds