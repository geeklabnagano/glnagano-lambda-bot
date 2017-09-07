from urllib.parse import urlparse

import dateutil.parser
import requests


def _get_event_connpass_keyword(param, today):
    encodedParams = urlparse(param)
    res = requests.get('http://connpass.com/api/v1/event/?' + encodedParams)
    data = res.json()
    # 日付が過去なら飛ばす
    event_datetime = dateutil.parser.parse(data['events'][0]['started_at'])
    if event_datetime < today:
        return None

    tweet = data['events'][0]['started_at'][5:7] + "月" + \
            data['events'][0]['started_at'][8:10] + "日 " + \
            data['events'][0]['title'] + "\n" + \
            data['events'][0]['event_url'] + "\n#" + data['events'][0]['hash_tag']

    return tweet


def get_event_connpass(series_id, today):
    res = requests.get("https://connpass.com/api/v1/event/?series_id=" + str(series_id))
    data = res.json()

    events = data['events']

    return _get_future_events(events, today)


def get_event_connpass_id(today, event_ids=None):
    if not event_ids:
        return None

    events = []
    for event_id in event_ids:
        res = requests.get("https://connpass.com/api/v1/event/?event_id=" + str(event_id))
        data = res.json()
        events.extend(data['events'])

    return _get_future_events(events, today)


def _change_date(date):
    return str(date)[5:7] + "月" + str(date)[8:10] + "日"


def _get_future_events(events, today):
    """イベント情報から開催日が過去の物を除外"""

    future_events = []
    for event in events:
        event_datetime = dateutil.parser.parse(event['started_at'])
        if event_datetime <= today:
            # 過去のものは除外
            continue
        event_date = _change_date(event_datetime)

        future_events.append(event['title'] + "(" + event_date + ")""\n" + \
                             event['event_url'] + " " + " ".join(_get_hash_tag_list(event['hash_tag'])))

    return future_events


def _get_hash_tag_list(hash_tag):
    hash_tag_list = hash_tag.split(" ")

    ret_list = []
    for tag in hash_tag_list:
        if tag[:1] != "#":
            ret_list.append("#" + tag)
            continue

        ret_list.append(tag)

    return ret_list
