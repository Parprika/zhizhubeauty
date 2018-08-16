from pymongo import MongoClient
from redis import StrictRedis


class MongoDB():
    def __init__(self):
        self.client = MongoClient(host='localhost', port=27017)
        self.db = self.client['zhihubeauty']
        self.collection = self.db['beauty']

    def getBeautyUrlToken(self):
        """
        返回粉丝数不为0的url_token
        """
        url_tokens = self.collection.find({'followers': {'$ne': []}})
        return url_tokens

    def getBeautyFollowers(self, beauty_url_token):
        """
        返回beauty_url_token的所有粉丝
        """
        return self.collection.find_one({
            'url_token': beauty_url_token
        })['followers']


class Redis():
    def __init__(self, key):
        self.client = StrictRedis(
            host='localhost',
            port=6379,
            db=1,
            password=None,
            decode_responses=True)
        self.key = key

    def add(self, url_token):
        """
        添加url_token，如果该url_token已存在，则score加1，否则添加该url_token，设置score为1
        """
        return self.client.zincrby(self.key, url_token, 1)

    def count(self):
        return self.client.zcard(self.key)

    def max(self, number):
        return self.client.zrevrange(self.key, 0, number, True)


def set_otaku_follows(beauty):
    for each in beauty:
        url_token = each['url_token']
        followers = mongo.getBeautyFollowers(url_token)
        for follower in followers:
            if follower['gender'] == 1:
                follower_url_token = follower['url_token']
                redis_followers.add(follower_url_token)


def set_beauty_followers(beauty, beat_otaku):
    for each in beauty:
        url_token = each['url_token']
        followers = mongo.getBeautyFollowers(url_token)
        for follower in followers:
            for otaku in beat_otaku:
                if otaku[0] == follower['url_token']:
                    redis_beauty.add(url_token)


mongo = MongoDB()
redis_followers = Redis('followers')
redis_beauty = Redis('beauty')
beauty = mongo.getBeautyUrlToken()
print('初始妹纸群体数量：', beauty.count())
set_otaku_follows(beauty)
print('初始宅男群体数量：', redis_followers.count())
best_otaku = redis_followers.max(2499)
beauty = mongo.getBeautyUrlToken()
set_beauty_followers(beauty, best_otaku)
best_beauty = redis_beauty.max(99)
print('最佳妹纸TOP100：', best_beauty)
