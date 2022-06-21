import requests
from utils.IdentifiVerify import IdentifiVerify
import random
import logging


class UniversityLogin:
    '''
    登录学校教务在线,作为身份认证
    用子类UscLogin
    不要用这个类
    '''
    def __init__(self, UserName, Password):
        logging.basicConfig(filename='UscLogin.log', level=logging.DEBUG)
        User_Agent = [
            'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 8.0; DUK-AL20 Build/HUAWEIDUK-AL20; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044353 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/WIFI Language/zh_CN Process/tools',
            'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-CN; EML-AL00 Build/HUAWEIEML-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.9.4.974 UWS/2.13.1.48 Mobile Safari/537.36 AliApp(DingTalk/4.5.11) com.alibaba.android.rimet/10487439 Channel/227200 language/zh-CN',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16D57'
        ]
        self.headers = {'User-Agent': random.choice(User_Agent)}
        self.s = requests.Session()
        self.UserName = UserName
        self.Password = Password

    def usc_login(self):
        self.s.get('http://jwzx.usc.edu.cn/')
        res = self.s.get('http://jwzx.usc.edu.cn/Core/verify_code.ashx?')
        Code = IdentifiVerify(res)
        data = {'UserName': self.UserName, 'Password': self.Password, 'Code': Code}
        res = self.s.post('http://jwzx.usc.edu.cn/Login/Login', data=data, headers=self.headers)
        if res.json().get('type') == 1:
            return True
        else:
            return False
