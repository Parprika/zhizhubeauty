import requests
import json
import time
from redis import StrictRedis

url = 'https://www.zhihu.com/api/v4/members/{url_token}/answers?include={include}&offset={offset}&limit=20&sort_by=created'
include = 'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,collapsed_by,suggest_edit,comment_count,can_comment,content,voteup_count,reshipment_settings,comment_permission,mark_infos,created_time,updated_time,review_info,question,excerpt,relationship.is_authorized,voting,is_author,is_thanked,is_nothelp;data[*].author.badge[?(type=best_answerer)].topics'
headers = {
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36'
}


def get_question(url_token, offset):
    try:
        response = requests.get(
            url.format(url_token=url_token, include=include, offset=offset),
            headers=headers)
        result = json.loads(response.text)
        if result.get('data') and len(result.get('data')):
            items = result.get('data')
            for item in items:
                question = item.get('question').get('title')
                print(question)
                db.zincrby('beauty_questions', question, 1)
        if result.get('paging').get('is_end') == False:
            get_question(url_token, offset + 20)
    except Exception:
        print('help!')
        time.sleep(20)


db = StrictRedis(
    host='localhost', port=6379, password=None, db=1, decode_responses=True)
beauty = db.zrevrange('beauty', 0, 99, True)
for each in beauty:
    url_token = each[0]
    get_question(url_token, 0)
question = db.zrevrange('beauty_questions', 0, 99, True)
for each in question:
    print(each[0])
