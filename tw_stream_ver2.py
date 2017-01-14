#!/usr/bin/python
#coding: utf-8

import requests
from requests_oauthlib import OAuth1Session
import json
import time, calendar

# OAuth 認証の初期化
def initialize():

    with open("secret.json") as f:
        secret_json = json.load(f)

    oath = OAuth1Session(secret_json["access_token"],
                            secret_json["access_token_secret"],
                            secret_json["consumer_key"],
                            secret_json["consumer_secret"])
    return oath

# 日時を見えやすく
def YmdHMS(tweet_time):
    time_utc = time.strptime(tweet_time, '%a %b %d %H:%M:%S +0000 %Y')
    unix_time = calendar.timegm(time_utc)
    time_local = time.localtime(unix_time)
    return time.strftime("%Y年%m月%d日 %H:%M:%S", time_local)

# 検索ワードを検索し，出力 (ツイート検索API使用)
def get_tweet_stream(oath):
    url = "https://stream.twitter.com/1.1/statuses/sample.json"

    res = oath.get(url, stream=True)

    if res.status_code != 200:
        print ("Error code: {0}". format(res.status_code))
        return None

    for line in res.iter_lines():
        try :
            tweet = json.loads(line.decode("utf-8"))
        except ValueError:
            pass
        #print (json.dumps(tweet, ensure_ascii=False, indent=2)) 

        try:
            if tweet["user"]["lang"] == "ja":
                #print (tweet["user"]["screen_name"])
                print (YmdHMS(tweet["created_at"]))
                print (tweet["text"])

        except:
            pass


def main():
    oath = initialize()
    get_tweet_stream(oath)

if __name__ == '__main__':
    main()
