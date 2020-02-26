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

def code2sessionToutiao(code):
    API = 'https://developer.toutiao.com/api/apps/jscode2session'
    params = 'appid=%s&secret=%s&code=%s' % \
             ('tt09fa7f4796d01677', '1201ac81849967734c7550c8b077a74101795ccb', code)
    url = API + '?' + params
    response = requests.get(url=url)
    data = json.loads(response.text)
    print(data)
    return data

if __name__ == '__main__':
    code2sessionToutiao("2548b29279fcf242")