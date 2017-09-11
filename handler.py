import os

import pytz
import twitter
from datetime import datetime as dt
from connpass import get_event_connpass, get_event_connpass_id


t = twitter.Api(access_token_key=os.getenv('ACCESS_TOKEN'),
                access_token_secret=os.getenv('ACCESS_TOKEN_SECRET'),
                consumer_key=os.getenv('CONSUMER_KEY'),
                consumer_secret=os.getenv('CONSUMER_SECRET'))


def handle(event, context):
    tweet_connpass()
    response = {
        "statusCode": 200,
        "body": '{}',
    }

    return response


def tweet_connpass():
    today = dt.now(pytz.timezone('Asia/Tokyo'))
    post_texts = []
    NSEG = 2391
    GLNAGANO = 2591

    for comm in [NSEG, GLNAGANO]:
        post_texts.extend(get_event_connpass(comm, today))

    # イベントのIDでツイート
    event_ids = [55693, 55694,]
    post_texts.extend(get_event_connpass_id(today, event_ids))

    for post_text in post_texts:
        # print(post_text)
        t.PostUpdates(status=post_text)
        # t.statuses.update(status='PyCon JP 2017 始まりました！（テスポ）')


if __name__ == '__main__':
    handle({}, {})
