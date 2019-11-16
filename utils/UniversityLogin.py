import requests
from utils.IdentifiVerify import IdentifiVerify
import random


class UniversityLogin:
    '''
    登录学校教务在线,作为身份认证
    '''
    def UscLogin(self, UserName, Password):
        User_Agent = [
            'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 8.0; DUK-AL20 Build/HUAWEIDUK-AL20; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044353 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/WIFI Language/zh_CN Process/tools',
            'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-CN; EML-AL00 Build/HUAWEIEML-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.9.4.974 UWS/2.13.1.48 Mobile Safari/537.36 AliApp(DingTalk/4.5.11) com.alibaba.android.rimet/10487439 Channel/227200 language/zh-CN',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16D57'
            ]
        headers = {'User-Agent': random.choice(User_Agent)}
        s = requests.Session()
        s.get('http://jwzx.usc.edu.cn/')
        res = s.get('http://jwzx.usc.edu.cn/Core/verify_code.ashx?')
        Code = IdentifiVerify(res)
        data = {'UserName': UserName, 'Password': Password, 'Code': Code}
        res = s.post('http://jwzx.usc.edu.cn/Login/Login', data=data, headers=headers)
        if res.json().get('type') == 1:
            return True
        else:
            return False

if __name__ == '__main__':
    uni = UniversityLogin()
    uni.UscLogin('20174670323', '18759799353')