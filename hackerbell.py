import requests, json
import util
HACKERBELL_RECEIVER = 'weiyi@papayamobile.com'
HACKERBELL_SNIPPET =""" 
<h4 style="margin:0;margin-bottom:6px;margin-top:6px">
<a style="font-size:14px;line-height:22px;font-weight:bold;text-decoration:none;color:#259;border:none;outline:none" href="%s" target="_blank">%s</a>&nbsp;&nbsp;</h4>
"""

def fetcc_top(n=10):
"""
{
  "by" : "resmi",
  "descendants" : 37,
  "id" : 9696397,
  "kids" : [ 9696849, 9696992, 9696819, 9697071, 9696772, 9697169, 9696584, 9696846, 9696726, 9697154 ],
  "score" : 83,
  "text" : "",
  "time" : 1433979537,
  "title" : "Google Launches Sidewalk Labs",
  "type" : "story",
  "url" : "https://plus.google.com/u/0/+LarryPage/posts/M1twDYHaui3"
}
"""
    r = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json')
    top = json.loads(r.content)
    items = []
    for id in top[:n]:
        r = requests.get('https://hacker-news.firebaseio.com/v0/item/%s.json' % id)
        i = json.loads(r.content)
        items.append(i)
    return items


def notify(body='N/A'):
    title = '[Hackerbell]Hacker News Top 10' 
    util.send_email(title, body, HACKERBELL_RECEIVER)


def wrap(items=None):
    if not items:
        return 'N/A'
    body = ''.join[HACKERBELL_SNIPPET % (i['url'], i['title']) for i in items]
    return body


def task():
    items = fetcc_top()
    body = wrap(items)
    notify(body)


