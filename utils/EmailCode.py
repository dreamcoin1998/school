from itsdangerous import URLSafeTimedSerializer as utsr
import base64
import re
from django.conf import settings as django_settings


class Token:

    def __init__(self, security_key):
        self.security_key = security_key
        self.salt = base64.b64encode(security_key.encode(encoding='utf-8'))

    # username安全序列化
    def generate_validate_token(self, username):
        serializer = utsr(self.security_key)
        return serializer.dumps(username, self.salt)

    # 解析username
    def confirm_validate_token(self, token, expiration=3600):
        serializer = utsr(self.security_key)
        # max_age，时间限制，在max_age之前的秒不能用，即3600=60*60，则有效时间为一个小时
        return serializer.loads(token, salt=self.salt, max_age=expiration)

    # 如果token过期， 则调用此方法，将username解析出来
    def remove_validate_token(self, token):
        serializer = utsr(self.security_key)
        print(serializer.loads(token, salt=self.salt))
        return serializer.loads(token, salt=self.salt)


token_confirm = Token(django_settings.SECRET_KEY)    # 定义为全局变量