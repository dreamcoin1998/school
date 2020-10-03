from utils.uscSystem.Timetable import Timetable
import requests
import random
from lxml import etree
import logging
import re


class NewTimetable(Timetable):
    '''
    继承自Timetable类，
    父类包含南华大学旧教务系统课表爬取方法，
    子类增加一个爬取南华大学新教务系统课表
    1.登录校园网
    2.携带session爬取课表数据
    '''
    def __init__(self, username, password):
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
        self.username = username
        self.password = password

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
                code = self.username + '%%%' + self.password
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
                    'userAccount': self.username,
                    'userPassword': self.password,
                    'encoded': encoded
                }
                res = self.s.post('http://61.187.179.66:8924/Logon.do?method=logon', headers=self.headers, data=data)
                # print(res.headers)
                # 登陆成功则为200
                if res.headers.get('cache-control') is None:
                    return True
                else:
                    return False
        except Exception as e:
            logging.debug(e)
            # print('login error:', e)
            return False

    def _solve_jieci(self, rets):
        """处理节次 课程对应是第几节取出来"""
        ret = []  # 节次
        for i in rets:
            i = i.replace('\r\n\t\t\t\t\t\t\t', '').replace('\xa0', '').replace('\n\t\t\t\t\t\t\t', '')
            if not i.endswith('节'):
                continue
            ret.append(i)
        return ret

    def _solve_single_double_week(self, part_sub, step=1):
        """单双周处理方式"""
        weekListData = []
        if len(part_sub.split('-')) == 2:
            for j in range(int(part_sub.split('-')[0]), int(part_sub.split('-')[1]) + 1, step):
                weekListData.append(str(j))
        else:
            weekListData.append(part_sub)
        return weekListData

    def _solve_week_data(self, data):
        """处理周数，将课程对应的周次取出来"""
        weekListData = []
        for part in data.split(","):
            # 如果匹配不到，返回原来的字符串，如果匹配到，则返回的字符串与原来的字符串不同
            if part != re.sub(r"\(周\)", "", part):
                part_sub = re.sub(r"\(周\)", "", part)
                weekListData += self._solve_single_double_week(part_sub)
            elif part != re.sub(r"\(单周\)", "", part):
                part_sub = re.sub(r"\(单周\)", "", part)
                weekListData += self._solve_single_double_week(part_sub, step=2)
            elif part != re.sub(r"\(双周\)", "", part):
                part_sub = re.sub(r"\(双周\)", "", part)
                weekListData += self._solve_single_double_week(part_sub, step=2)
        return weekListData

    # 爬取课表并且解析处理
    def getTimetable(self):
        """
        爬取数据，分析数据，格式化数据，返回数据格式
        :return:

        [
            ['1一2节', 'Monday', 'UML软件建模', '3-9(周)', '【环安楼】8-410', 'none'],
            ['1一2节', 'Monday', 'UML软件建模', '3-9(周)', '【环安楼】8-410', 'none']
        ]
        """
        try:
            url = 'http://61.187.179.66:8924/jsxsd/xskb/xskb_list.do'
            res = self.s.post(url, headers=self.headers, data={'rq': '2020-02-11'})
            html = etree.HTML(res.text)
            rets = html.xpath('//tr/th//text()')[8:-1]
            ret = self._solve_jieci(rets)
            weeks = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            dataList = []
            for index, section in enumerate(ret):
                # section -> '1一2节'
                for indexWeeks, week in enumerate(weeks):
                    # week -> Monday
                    # 下面这里indexWeeks要加二，不然前端会出错
                    the_class_info = html.xpath(
                        '//tr[%s]/td[%s]/div[1]//text()' % (str(index + 2), (indexWeeks + 2))
                    )
                    # ['UML软件建模', '3-9(周)', '【环安楼】8-410', '----------------------', '建筑消防工程', '8-11(周)', '【南华楼】1-614']
                    # 或者是['\xa0']或者[]
                    classes = [i for i in the_class_info if not i.startswith('---') and i != '&nbspO']
                    className = classes[::3]  # 获取课程名称
                    classInfo = [k for i, k in enumerate(classes) if i % 3 != 0]
                    i = 0
                    for indexClassName, cN in enumerate(className):
                        if cN == '\xa0':
                            continue
                        data = [cN]
                        data += classInfo[i: i + 2]
                        data.append('none')
                        weekListData = self._solve_week_data(data[-3])
                        data[-3] = ' '.join(weekListData)
                        dataList.append([section, week] + data)
                        i += 2
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
        if login:
            return [self.getTimetable()]
        else:
            return login
