import requests
from school import settings
import json


def c2s(appid, code):
    return code2session(appid, code)

def code2session(appid, code):
    API = 'https://api.q.qq.com/sns/jscode2session'
    params = 'appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' % \
             (appid, settings.QQ_SECRET, code)
    url = API + '?' + params
    response = requests.get(url=url)
    data = json.loads(response.text)
    print(data)
    return data