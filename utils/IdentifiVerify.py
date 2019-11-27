from datetime import datetime
import hashlib
import base64
import requests
import json


def IdentifiVerify(res):
    '''
    调用斐斐打码识别验证码
    :param res:
    :return:
    '''
    now = datetime.now()
    time = str(int(datetime.timestamp(now)))
    userID = '118006'
    pd_key = 'Fhq9N8NsY7M3TEQ6HonzKCaXDX3nuHa7'
    predict_type = '30400'
    md5 = hashlib.md5()
    md5.update(f'{time}{pd_key}'.encode('utf-8'))
    n = md5.hexdigest()
    md5 = hashlib.md5()
    md5.update(f'{userID}{time}{n}'.encode('utf-8'))
    sign = md5.hexdigest()
    b64 = base64.b64encode(res.content)
    img_data = b64.decode('utf-8')
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    data = {'user_id': userID, 'timestamp': time, 'sign': sign, 'predict_type': predict_type, 'img_data': img_data}
    res = requests.post('http://pred.fateadm.com/api/capreg', data=data, headers=headers)
    return json.loads(res.json().get('RspData')).get('result')