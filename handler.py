import os

import boto3
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

    # from boto3.session import Session
    # session = Session(profile_name='my_local_profile')
    # s3 = session.resource('s3')
    s3 = boto3.resource('s3')

    bucket = s3.Bucket(os.getenv('AWS_S3_BUCKET_NAME'))
    obj = bucket.Object('last_reply_id')
    response = obj.get()
    body = response['Body'].read()
    since_id = int(body.decode('utf-8'))
    replies = t.GetMentions(since_id=since_id, trim_user=2208330278)
    for reply in replies:
        response = obj.put(
            Body=str(since_id).encode('utf-8'),
            ContentEncoding='utf-8',
            ContentType='text/plain'
        )
        res = c.send(ut=reply.text, apiname='Dialogue')
        user = t.GetUser(user_id=reply.user.id)
        t.PostUpdate('@{} {} (bot)'.format(user.screen_name, res['utt']), in_reply_to_status_id=reply.id)


def tweet_lunch():
    now = dt.now(pytz.timezone('Asia/Tokyo'))
    if now.second == 10:
        menu = '💩'
    elif now.second%10 in (1, 2):
        menu = '🍻'
    elif now.second%10 in (3, ):
        menu = '🍣'
    elif now.second%10 in (4, ):
        menu = '🍦'
    elif now.second%10 in (5, ):
        menu = '🍭'
    elif now.second%10 in (6, ):
        menu = '🍱'
    elif now.second%10 in (7, ):
        menu = '🍣'
    elif now.second%10 in (8, ):
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
    JAWS_UG_NAGANO = 4553

    for comm in [NSEG, GLNAGANO, JAWS_UG_NAGANO]:
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
