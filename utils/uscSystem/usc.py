from utils.uscSystem.NewUSCSystemTimetable import NewTimetable
from lxml import etree


class Usc(NewTimetable):

    def __getattr__(self, item):
        if item == 'check_score_link':
            setattr(self, 'check_score_link', 'http://61.187.179.66:8924/jsxsd/kscj/cjcx_list')
            return self.check_score_link
        else:
            raise AttributeError('type object "%s" has no attribute "%s"' % (self, item))

    def parse_score(self, data):
        '''
        tip: 爬取成绩接口解析成绩并返回
        :return:
        '''
        res = self.s.post(self.check_score_link, headers=self.headers, data=data)
        html = etree.HTML(res.text)
        order_num = html.xpath('//div/table//tr/td[1]/text()')
        score_data = []
        '''
        字段属性：
        4 = 课程名称
        6 = 成绩
        8 = 学分
        12 = 考核方式
        14 = 课程属性
        '''
        extra_data = ['4', '6', '8', '12', '14']
        for index in order_num:
            class_info = []
            for list_index in extra_data:
                # index是从2开始，order_num是从1开始
                class_field = html.xpath('//div/table//tr[%s]/td[%s]/text()' % (str(int(index) + 1), list_index))[0]
                # 将\t \n 替换为'',注意格式
                class_field = class_field.replace('\n', '').replace('\t', '')
                class_info.append(class_field)
            score_data.append(class_info)
        # print(score_data)
        return score_data

    def check_score(self, data):
        '''
        tip: 查成绩
        1. 登录
        2. 根据登录接口解析出成绩
        '''
        if self.login():
            return self.parse_score(data)
        else:
            return False


# data = {
#     'kksj': '2019-2020-1',
#     'kcxz': '',
#     'kcmc': '',
#     'xsfs': 'all'
# }
# Usc('20174670323', '18759799353gjb').check_score(data)
