# 项目各密码配置文件
# 放置于项目根目录下

### django APP秘钥
SECRET_KEY = '-qhsgt6r3a4lb1*181+hl141#o@7@am29wa8v$^@dgp(1e)=yj'
QQ_SECRET = 'B5T4EEMD2MHnmGyX'
wx_SECRET = 'e39369c9d39feabc58771b1caddf0961'

### mysql 配置
MYSQL_HOST = 'cdb-07n3b91f.gz.tencentcdb.com'
MYSQL_PORT = 10081
MYSQL_USER = 'root'
MYSQL_PASSWORD = '18759799353gjb!'

### 邮件发送配置
# 发件人授权码
EMAIL_HOST_PASSWORD = 'xfYC4mkT2QLPuBQv'

### Celery配置
# redis的地址
BROKER_URL = 'redis://www.gaoblog.cn:6379/6'

#celery结果返回，可用于跟踪结果
CELERY_RESULT_BACKEND = 'redis://www.gaoblog.cn:6379/0'

# 新校园网学期默认值
'''
参数说明：
kksj(开课时间):2020-2021-1 [year]-[year+1]-[1|2] 1为秋季学期 2为春季学期
kcxz(课程性质):02 公共基础课平台 04 专业课平台 07 学科基础平台 不填为全选
kcmc: 课程名称
xsfs(显示方式): all 全部 max 最好成绩
'''
USC_ARGS = {
    'kksj': '2019-2020-1',
    'kcxz': '',
    'kcmc': '',
    'xsfs': 'all'
}

'''
评论信息所对应的类
'''
OBJ_TYPE = {
    'commody': 'Commody',
    'post': 'Post'
}