import gevent
from gevent import monkey
monkey.patch_all()
import urllib2
import requests, json
import util
HACKERBELL_JOBS = ['job', 'hire', 'hiring', 'full-time', 'full time']
HACKERBELL_KEYS = ['python', 'amazon', 'nginx', 'aws', 'china', 'amazon', 'performance', 'language', 'hack']
HACKERBELL_RECEIVER = 'weiyi@papayamobile.com'
HACKERBELL_GUEST = 'haozhang85@gmail.com'
HACKERBELL_SNIPPET =""" 
<h4 style="margin:0;margin-bottom:6px;margin-top:6px">
<a style="font-size:14px;line-height:22px;font-weight:bold;text-decoration:none;color:#259;border:none;outline:none" href="%s" target="_blank">%s</a>&nbsp;&nbsp;</h4>
"""

def fetch_top_ids():
    r = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json')
    top = json.loads(r.content)
    return top

def fetch_new_ids():
    r = requests.get('https://hacker-news.firebaseio.com/v0/newstories.json')
    new = json.loads(r.content)
    return new

def fetch_story(id):
    r = urllib2.urlopen('https://hacker-news.firebaseio.com/v0/item/%s.json' % id).read()
    return json.loads(r)

def notify(title='[Hackerbell]Hacker News Top 10', body='N/A', to=HACKERBELL_RECEIVER): 
    util.send_email(title, body, to)

def wrap(items=None):
    if not items:
        return 'N/A'
    body = ''.join([HACKERBELL_SNIPPET % (i['url'], i['title'] + ' [score: %s]' % i['score']) for i in items])
    return body

def task():
    items = fetch_top(10)
    body = wrap(items)
    notify(body=body)

def task1():
    task_top_key(keys=HACKERBELL_KEYS)

def task2():
    task_new_key(keys=HACKERBELL_KEYS)

def task3():
    task_job_key(keys=HACKERBELL_JOBS)

def fetch_top(n=500):
    top = fetch_top_ids()[:n]
    jobs = [gevent.spawn(fetch_story, id) for id in top]
    gevent.wait(jobs)
    return [j.value for j in jobs]

def fetch_new(n=500):
    top = fetch_new_ids()[:n]
    jobs = [gevent.spawn(fetch_story, id) for id in top]
    gevent.wait(jobs)
    return [j.value for j in jobs]
    
def task_top_key(keys=None):
    items = fetch_top()
    items = filter_keys(items, keys)
    body = wrap(items)
    notify(title='[Hackerbell]Top keys', body=body)

def task_new_key(keys=None):
    items = fetch_new()
    items = filter_keys(items, keys)
    body = wrap(items)
    notify(title='[Hackerbell]New keys', body=body)

def task_job_key(keys=None):
    items1 = fetch_new(n=1000)
    items2 = fetch_top(n=100)
    items = items1 + items2
    items = filter_keys(items, keys)
    body = wrap(items)
    notify(title='[Hackerbell]Jobs', body=body)
    notify(title='[Hackerbell]Jobs', body=body, to=HACKERBELL_GUEST)

def filter_keys(items, keys):
    if not keys:
        return items
    keys = set(keys)
    r = [i for i in items if _check(i['title'], keys)]
    return r

def _check(title, keys):
    title =title.lower()
    for k in keys:
        if k in title:
            return True
    return False
