from utils.uscSystem.Timetable import Timetable
import requests
import random
from lxml import etree
import logging


class NewTimetable(Timetable):
    '''
    继承自Timetable类，
    父类包含南华大学旧教务系统课表爬取方法，
    子类增加一个爬取南华大学新教务系统课表
    1.登录校园网
    2.携带session爬取课表数据
    '''
    def __init__(self, UserName, Password):
        logging.basicConfig(filename='NewTimetable.log', level=logging.DEBUG)
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

    # 登录校园网
    def login(self):
        try:
            # 登录校园网，首先获取传输参数encode
            res = self.s.post('http://61.187.179.66:8924/Logon.do?method=logon&flag=sess', headers=self.headers)
            dataStr = res.text
            # print(dataStr)
            if dataStr == 'no':
                return False
            else:
                scode = dataStr.split('#')[0]
                sxh = dataStr.split('#')[1]
                code = self.UserName + '%%%' + self.Password
                encoded = ''
                i = 0
                while i < len(code):
                    if i < 20:
                        encoded = encoded + code[i:i + 1] + scode[0:int(sxh[i:i + 1])]
                        scode = scode[int(sxh[i:i + 1]):len(scode)]
                    else:
                        encoded = encoded + code[i:len(code)]
                        i = len(code)
                    i += 1
                # print(encoded)
                # 校园网登录
                data = {
                    'userAccount': self.UserName,
                    'userPassword': self.Password,
                    'encoded': encoded
                }
                res = self.s.post('http://61.187.179.66:8924/Logon.do?method=logon', headers=self.headers, data=data)
                print(res.headers)
                # 登陆成功则为200
                if res.headers.get('cache-control') is None:
                    return True
                else:
                    return False
        except Exception as e:
            logging.debug(e)
            print('login error:', e)
            return False

    # 爬取课表并且解析处理
    def getTimetable(self):
        # 课表链接
        try:
            url = 'http://61.187.179.66:8924/jsxsd/xskb/xskb_list.do'
            res = self.s.post(url, headers=self.headers, data={'rq': '2020-02-11'})
            html = etree.HTML(res.text)
            # print(html)
            rets = html.xpath('//tr/th//text()')[8:-1]
            # print(rets)
            ret = []  # 节次
            # weeks = html.xpath('//tr[1]/th//text()')[1:]  # 星期
            # print(weeks)
            weeks = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            for i in rets:
                i = i.replace('\r\n\t\t\t\t\t\t\t', '').replace('\xa0', '').replace('\n\t\t\t\t\t\t\t', '')
                if not i.endswith('节'):
                    continue
                ret.append(i)
            # print(ret)
            dataList = []
            for index, jieci in enumerate(ret):
                # print(jieci)
                ret1 = {}  # 格式 {节次： 课时}
                classJieci = []
                for indexWeeks, week in enumerate(weeks):
                    # className = html.xpath(
                    #     '//tr[%s]/td[%s]/div[2]/text()[1]' % (str(index + 2), (indexWeeks + 1)))
                    # print(className)
                    # classInfo = html.xpath(
                    #     '//tr[%s]/td[%s]/div[2]/font/text()[1]' % (str(index + 2), (indexWeeks + 1)))
                    clses = html.xpath(
                        '//tr[%s]/td[%s]/div[1]//text()' % (str(index + 2), (indexWeeks + 2))
                    )
                    # print(classes)
                    classes = [i for i in clses if not i.startswith('---') and i != '&nbspO']
                    # print(classes)
                    # for i in clses:
                    #     print(i)
                    i = 0
                    className = classes[::3]
                    # print(className)
                    classInfo = [k for i, k in enumerate(classes) if i % 3 != 0]
                    # print(classInfo)
                    # if classInfo != []:
                        # classInfo[1] = classInfo[1][:-11]
                    print(classInfo)
                    for indexClassName, cN in enumerate(className):
                        if cN == '\xa0':
                            continue
                        weekClass = {}
                        data = []
                        # print(id(data), cN)
                        data.append(cN)
                        # print(i)
                        data += classInfo[i: i + 2]
                        data.append('none')
                        # 处理周数
                        # print(data)
                        weekList = data[-3].replace('(周)', '').split(',')
                        # print(weekList)
                        weekListData = []
                        for wl in weekList:
                            if len(wl.split('-')) == 2:
                                # print(wl, classes)
                                for j in range(int(wl.split('-')[0]), int(wl.split('-')[1]) + 1):
                                    # print(j)
                                    weekListData.append(str(j))
                            else:
                                weekListData.append(wl)
                            # print(weekListData)
                        data[-3] = ' '.join(weekListData)
                        # print(data)
                        # print(classInfo)
                        weekClass[week] = data
                        classJieci.append(weekClass)
                        i += 2
                    # print(weekClass)
                ret1[jieci] = classJieci
                dataList.append(ret1)
            print(dataList)
            return dataList
        except Exception as e:
            logging.debug(e)
            print('uscSystem error: ', e)
            return False

    def run(self):
        '''
        1.登录校园网
        2.携带session爬取课表数据并处理
        :return:
        '''
        login = self.login()
        print(login)
        if login:
            return [self.getTimetable()]
        else:
            return login


NewTimetable('20174670323', '18759799353gjb').run()
