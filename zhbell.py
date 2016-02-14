# -*- coding: utf-8 -*-
import requests
import json
import util
from bs4 import BeautifulSoup
import random

ZHH_NUM = 20

ZHBELL_SNIPPET ="""
<img src="%s" width="128" height="128"> 
<h4 style="margin:0;margin-bottom:6px;margin-top:6px">
<a style="font-size:14px;line-height:22px;font-weight:bold;text-decoration:none;color:#259;border:none;outline:none" href="%s" target="_blank">%s</a>&nbsp;&nbsp;</h4>
"""

ZHBELL_RECEIVER = 'weiyi@papayamobile.com'

ZHPIC = ['https://pic4.zhimg.com/7d8c15df29ce6900c80f9cf630992687_xl.jpg',
         'https://pic1.zhimg.com/e8b840284350f4a2d01ea6869926bfcc_xl.jpg',
         'https://pic1.zhimg.com/1f9c99e8aa4b0ab76d4885ffd0eb10c0_xl.jpg',
         'https://pic1.zhimg.com/5c5f5d55992d64aa8184b29c53e80af4_xl.jpg',
         'https://pic1.zhimg.com/a240a363b7d7e0681502017c57b0ba20_xl.jpg',
         'https://pic4.zhimg.com/5bda61313f8e3767edaa6134941e207b_xl.jpg',
         'https://pic3.zhimg.com/d8426d43e_xl.jpg',
         'https://pic3.zhimg.com/cf0156d3a_xl.jpg',
         'https://pic2.zhimg.com/ca0657b5e0ef154ee25c3e357a6c607d_xl.jpg',
         'https://pic4.zhimg.com/f07808da5625fef3607f8b75b770349f_xl.jpg',
         'https://pic1.zhimg.com/975baaf73fd76f48ce6f05e19b176878_xl.jpg',
         'https://pic3.zhimg.com/2bd2e49d3f849155376393085edc1d9e_xl.jpg',
         ]

def get_zh_pic():
    i = random.randrange(0, len(ZHPIC))
    return ZHPIC[i]

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
    task_zhihuhot()

def task_new():
    r = get_new_stories()
    r = wrap(r)
    notify(title='[ZHBell]New', body=r)

def task_zhihuhot():
    r = get_zhihuhot()
    r = wrap_zhihuhot(r)
    notify(title='[ZHBell]知乎热门', body=r)

def wrap_zhihuhot(items=None):
    if not items:
        return 'N/A'
    body = ZHBELL_SNIPPET % (get_zh_pic(), 'http://zhihuhot.sinaapp.com/', '知乎热门TOP500')
    body = body.decode('utf8')
    body += ''.join([ZHBELL_SNIPPET % (get_zh_pic(), i[1], i[0]) for i in items])
    return  body

def get_zhihuhot():
    r = requests.get('http://zhihuhot.sinaapp.com/')
    soup = BeautifulSoup(r.text)
    r = soup.findAll("div")[1:ZHH_NUM+1]
    r = [(a.get_text(), a.find('a')['href']) for a in r]
    return r

