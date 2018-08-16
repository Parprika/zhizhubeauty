# -*- coding: utf-8 -*-
"""
2018-06-19
"""
import json
from scrapy.spider import Spider
from scrapy.http import Request
from zhihubeauty.items import BeautyItem, RelationItem


class BeautySpider(Spider):
    name = 'beauty'
    allowed_domains = ['www.zhihu.com']
    question_url = 'https://www.zhihu.com/api/v4/questions/{questionid}/answers?include={include}&limit=5&offset={offset}&sort_by=default'
    question_query = 'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[*].mark_infos[*].url;data[*].author.follower_count,badge[?(type=best_answerer)].topics'
    followers_url = 'https://www.zhihu.com/api/v4/members/{url_token}/followers?include={include}&offset={offset}&limit=20'
    followers_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    questions = [
        '263952082', '24463692', '19671417', '35255031', '61847755',
        '35931586', '26037846', '28467579', '66963840', '24400664', '38376393',
        '28592040', '29815334', '34353723', '50426133'
    ]

    def start_requests(self):
        for question in self.questions:
            yield Request(
                self.question_url.format(
                    questionid=question, include=self.question_query,
                    offset=0),
                callback=self.parse_beauty,
                meta={
                    'questionid': question,
                    'offset': 0,
                })

    def parse_beauty(self, response):
        result = json.loads(response.text)
        if result.get('data') and len(result.get('data')):
            items = result.get('data')
            for item in items:
                if item.get('author')['gender'] == 0:
                    url_token = item.get('author')['url_token']
                    beauty_item = BeautyItem()
                    beauty_item['url_token'] = url_token
                    beauty_item['name'] = item.get('author')['name']
                    beauty_item['gender'] = item.get('author')['gender']
                    beauty_item['avatar_url'] = item.get('author')[
                        'avatar_url']
                    beauty_item['headline'] = item.get('author')['headline']
                    beauty_item['followers'] = []
                    yield beauty_item
                    yield Request(
                        self.followers_url.format(
                            url_token=url_token,
                            include=self.followers_query,
                            offset=0),
                        callback=self.parse_followers,
                        meta={
                            'url_token': url_token,
                            'offset': 0
                        })
        questionid = response.meta.get('questionid')
        offset = response.meta.get('offset') + 5
        if result.get('paging').get('is_end') == False:
            yield Request(
                self.question_url.format(
                    questionid=questionid,
                    include=self.question_query,
                    offset=offset),
                callback=self.parse_beauty,
                meta={
                    'questionid': questionid,
                    'offset': offset
                })

    def parse_followers(self, response):
        result = json.loads(response.text)
        url_token = response.meta.get('url_token')
        offset = response.meta.get('offset') + 20
        if result.get('data') and len(result.get('data')):
            followers = result.get('data')
            relation_item = RelationItem()
            followers = [{
                'url_token': follower.get('url_token'),
                'name': follower.get('name'),
                'headline': follower.get('headline'),
                'gender': follower.get('gender'),
                'avatar_url': follower.get('avatar_url')
            } for follower in followers]
            relation_item['url_token'] = url_token
            relation_item['followers'] = followers
            yield relation_item
        if result.get('paging').get('is_end') == False:
            yield Request(
                self.followers_url.format(
                    url_token=url_token,
                    include=self.followers_query,
                    offset=offset),
                callback=self.parse_followers,
                meta={
                    'url_token': url_token,
                    'offset': offset
                })
