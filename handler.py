import os

import pytz
import twitter
from datetime import datetime as dt
from connpass import get_event_connpass, get_event_connpass_id
from doco.client import Client


t = twitter.Api(access_token_key=os.getenv('ACCESS_TOKEN'),
                access_token_secret=os.getenv('ACCESS_TOKEN_SECRET'),
                consumer_key=os.getenv('CONSUMER_KEY'),
                consumer_secret=os.getenv('CONSUMER_SECRET'))


def handle(event, context):
    # reply()
    now = dt.now(pytz.timezone('Asia/Tokyo'))
    if 0 <= now.hour == 10:
        pass
    elif now.hour == 11:
        tweet_lunch()
        tweet_connpass()
    elif 12 <= now.hour <= 20:
        pass
    elif now.hour == 21:
        t.PostUpdates(status='1日8時間睡眠のためにも寝る準備をしましょう！')
    elif now.hour == 22:
        pass
    elif now.hour == 23:
        tweet_connpass()
    else:
        pass
    response = {
        "statusCode": 200,
        "body": '{}',
    }

    return response


def reply():
    c = Client(apikey=os.getenv('DOCO_API_KEY'))
    since_id = 1909013802699546524  # どっかに保存しておく
    replies = t.GetMentions(since_id=since_id, trim_user=2208330278)
    for reply in replies:
        print(reply.id)  # どっかに保存しておく
        res = c.send(ut=reply.text, apiname='Dialogue')
        t.PostUpdate(res['utt'], in_reply_to_status_id=reply.id)


def tweet_lunch():
    now = dt.now(pytz.timezone('Asia/Tokyo'))
    if now.second == 10:
        menu = '💩'
    elif now.second%10 in (1, 3):
        menu = '🍺'
    elif now.second%10 in (2, 4, 6):
        menu = '🍣'
    elif now.second%10 in (5, 7):
        menu = '🍜'
    else:
        menu = '🍙'
    t.PostUpdates(status='今日のお昼は{}にしよう！'.format(menu))


def tweet_connpass():
    today = dt.now(pytz.timezone('Asia/Tokyo'))
    # 2日にいっぺんくらいつぶやいとく
    if today.day%2 == 0:
        return
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
