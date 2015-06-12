import requests
import json
import util

ZHBELL_SNIPPET ="""
<img src="%s" width="128" height="128"> 
<h4 style="margin:0;margin-bottom:6px;margin-top:6px">
<a style="font-size:14px;line-height:22px;font-weight:bold;text-decoration:none;color:#259;border:none;outline:none" href="%s" target="_blank">%s</a>&nbsp;&nbsp;</h4>
"""

ZHBELL_RECEIVER = 'weiyi@papayamobile.com'

def get_latest():
    headers = {'User-agent': 'Mozilla/5.0'}
    r = requests.get('http://news-at.zhihu.com/api/4/news/latest', headers=headers)
    return json.loads(r.content)

def get_new_stories():
    r = get_latest()
    return r['stories']

def get_top_stories():
    r = get_latest()
    return r['top_stories']

def notify(title='[ZHBell]Latest', body='N/A'):
    util.send_email(title, body, ZHBELL_RECEIVER)

def wrap(items=None):
    if not items:
        return 'N/A'
    body = ''.join([ZHBELL_SNIPPET % (i['images'][0] if i.get('images') else i['image'], 'http://daily.zhihu.com/story/%s' % i['id'], i['title']) for i in items])
    return body

def task_top():
    r = get_top_stories()
    r = wrap(r)
    notify(title='[ZHBell]Top', body=r)

def task_new():
    r = get_new_stories()
    r = wrap(r)
    notify(title='[ZHBell]New', body=r)
