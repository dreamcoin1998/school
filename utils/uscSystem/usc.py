from utils.uscSystem.NewUSCSystemTimetable import NewTimetable


class Usc(NewTimetable):

    def parse_score(self):
        '''
        tip: 爬取成绩接口解析成绩并返回
        :return:
        '''
        pass

    def check_score(self):
        '''
        tip: 查成绩
        1. 登录
        2. 根据登录接口解析出成绩
        '''
        if self.login():
            return self.parse_score()
        else:
            return False
