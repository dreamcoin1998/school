from lxml import etree
import requests
import random
from utils.IdentifiVerify import IdentifiVerify
import re


class Timetable:
    '''
    获取课表
    用子类NewTimetable()
    '''
    @classmethod
    def USC_Timetable(self, UserName, Password, termCode):
        '''
        南华大学课表
        :param UserName:
        :param Password:
        :param termCode:
        :return:
        '''
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
        # 先登录教务在线
        res = s.get('http://jwzx.usc.edu.cn/Core/verify_code.ashx?')
        Code = IdentifiVerify(res)
        data = {'UserName': UserName, 'Password': Password, 'Code': Code}
        res = s.post('http://jwzx.usc.edu.cn/Login/Login', data=data, headers=headers)
        # 登陆成功，获取课表
        if res.json().get('type') == 1:
            data = {'termCode': termCode, 'sort': 'TimeName', 'order': 'ASC'}
            res = s.post('http://jwzx.usc.edu.cn/Student/StuTimetable/GetStudentTimetable', headers=headers, data=data)
            # print(res.json())
            rows = res.json().get('rows')
            result = []
            for r in rows:
                TimeName = r['TimeName']
                del r['TimeCode']
                del r['TimeName']
                # print(r)
                timeName = {}
                timeNameClasses = []
                for k, v in r.items():
                    if len(v):
                        root = etree.HTML(v)
                        classes = root.xpath('//ul//li/text()')
                        # print(classes)
                        n = len(classes) // 5 # 前5个为一个课时
                        cls = [classes[5*(n-1): 5*n] for n in range(1, n+1)] # 课时信息
                        # timeName[TimeName] = []
                        for c in cls:
                            cla = {}
                            week = []
                            for time_section in c[3].split('.'):
                                time_section = time_section.replace(' (红湘)', '')
                                start_end = time_section.split('-')
                                if len(start_end) == 2:
                                    for time in range(int(start_end[0]), int(start_end[1]) + 1):
                                        week.append(str(time))
                                else:
                                    week.append(str(start_end[0]))
                            print(c[4])
                            c[4] = re.match(r'^(\d+\-\d{3}\-{0,1}\w{0,1})\s\(\w+\s{0,5}\)$', c[4]).groups()[0]
                            c[3] = ' '.join(week)
                            # print(c)
                            cla[k] = c
                            timeNameClasses.append(cla)
                            # print(dic)
                        timeName[TimeName] = timeNameClasses
                result.append(timeName)
            print(result)
            return result
        else:
            return False


if __name__ == '__main__':
    print(Timetable.USC_Timetable('20174670323', '18759799353', '2019-2020-1'))