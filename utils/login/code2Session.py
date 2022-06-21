import requests
from school import settings
import json


def c2s(app_id, code, platform='QQ'):
    if platform == 'QQ':
        return code2sessionQQ(app_id, code)
    elif platform == 'WX':
        return code2sessionWeiXin(app_id, code)
    elif platform == 'Toutiao':
        return code2sessionToutiao(app_id, code)
    raise ValueError("获取openid失败， platform %s（平台） 尚未匹配" % platform)


def code2sessionQQ(appid, code):
    API = 'https://api.q.qq.com/sns/jscode2session'
    params = 'appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' % \
             (appid, settings.QQ_SECRET, code)
    url = API + '?' + params
    response = requests.get(url=url)
    data = json.loads(response.text)
    return data


def code2sessionToutiao(appid, code):
    API = 'https://developer.toutiao.com/api/apps/jscode2session'
    params = 'appid=%s&secret=%s&code=%s' % \
             (appid, settings.TouTiao_SECRET, code)
    url = API + '?' + params
    response = requests.get(url=url)
    data = json.loads(response.text)
    return data


def code2sessionWeiXin(appid,code):
    API = 'https://api.weixin.qq.com/sns/jscode2session'
    params = 'appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' % \
             (appid, settings.wx_SECRET, code)
    url = API + '?' + params
    response = requests.get(url)
    data = json.loads(response.text)
    return data
