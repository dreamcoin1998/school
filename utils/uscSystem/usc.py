from billiard.sharedctypes import copy
from utils.uscSystem.NewUSCSystemTimetable import NewTimetable
from lxml import etree
from school import config


class Usc(NewTimetable):

    def __getattr__(self, item):
        if item == 'check_score_link':
            setattr(self, 'check_score_link', 'http://61.187.179.66:8924/jsxsd/kscj/cjcx_list')
            return self.check_score_link
        else:
            raise AttributeError('type object "%s" has no attribute "%s"' % (self, item))

    @staticmethod
    def set_default_args(data):
        # 加载默认参数，复制一个新的字典，防止修改配置
        default_args = config.USC_ARGS.copy()
        # print(default_args is config.USC_ARGS)
        # 未传参数则直接使用默认参数
        if data is None:
            return default_args
        for query in default_args.keys():
            # 如果用户参数重写了参数则使用用户参数
            if query in data:
                default_args[query] = data[query]
        return default_args

    def parse_score(self, data):
        '''
        tip: 爬取成绩接口解析成绩并返回
        :return:
        '''
        res = self.s.post(self.check_score_link, headers=self.headers, data=data)
        html = etree.HTML(res.text)
        # ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
        # 每一科的在第几行
        order_num = html.xpath('//div/table//tr/td[1]/text()')
        # print(order_num)
        score_data = []
        '''
        每一科的成绩有很多个字段，以下是所截取的字段
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
                class_field = class_field.replace('\n', '').replace('\t', '').replace('\r', '')
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
        # 参数校验
        data = self.set_default_args(data)
        if self.login():
            return self.parse_score(data)
        else:
            return False


if __name__ == '__main__':
    data = Usc('20174670323', '18759799353gjb').check_score(None)
    print(data)
