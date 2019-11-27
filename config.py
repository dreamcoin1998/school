# 项目各密码配置文件
# 放置于项目根目录下

### django APP秘钥
SECRET_KEY = '-qhsgt6r3a4lb1*181+hl141#o@7@am29wa8v$^@dgp(1e)=yj'
QQ_SECRET = 'B5T4EEMD2MHnmGyX'

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