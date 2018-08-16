# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import logging
import requests
import random
import json
import time
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


class ProxyMiddleware(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.url = 'http://piping.mogumiao.com/proxy/api/get_ip_bs?appKey=e505ec870e444b56b48e3b5227aefbd9&count=10&expiryDate=0&format=1&newLine=2'
        self.proxy = self.get_proxies()
        self.counts = 0

    def get_proxies(self):
        proxies = []
        try:
            html = requests.get(self.url).text
            items = json.loads(html).get('msg')
            for item in items:
                ip = item.get('ip')
                port = str(item.get('port'))
                proxies.append(ip + ':' + port)
            return proxies
        except:
            time.sleep(5)
            return self.get_proxies()

    def process_request(self, request, spider):
        if request.meta.get('retry_times'):
            self.proxy = self.get_proxies()
            pre_proxy = random.choice(self.proxy)
            request.meta['proxy'] = 'https://{}'.format(pre_proxy)
            self.counts = 0
        elif self.counts < 400:
            pre_proxy = random.choice(self.proxy)
            request.meta['proxy'] = 'https://{}'.format(pre_proxy)
            self.counts += 1
        else:
            self.counts = 0
            self.proxy = self.get_proxies()


class RandomUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        return cls(user_agent=crawler.settings.get('MY_USER_AGENT'))

    def process_request(self, request, spider):
        agent = random.choice(self.user_agent)
        request.headers['User-Agent'] = agent
