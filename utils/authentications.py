from django.contrib.auth.backends import ModelBackend
from rest_framework.authentication import get_authorization_header
import jwt
from utils.permissions.permissions import get_user_obj
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication, jwt_decode_handler
from rest_framework.exceptions import AuthenticationFailed
from yonghu.serializers import QQUserSerializer


class MyYonghuBackend(ModelBackend):
    """
    自定义登陆验证
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user_obj = get_user_obj(request)
            return user_obj
        except KeyError as e:
            return None


def jwt_response_payload_handler(token, yonghu=None, request=None):
    return {
        "token": token,
        "yonghu": QQUserSerializer(yonghu).data,
    }


class JWTModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """

        :param request:
        :param username:
        :param password:
        :param kwargs:
        :return:
        """
        pass


class JSONWebTokenAuthentication(BaseJSONWebTokenAuthentication):

    def authenticate_credentials(self, payload):
        pass

    def authenticate(self, request):
        # 采用drf获取token的手段 - HTTP_AUTHORIZATION - Authorization
        token = get_authorization_header(request)
        if not token:
            raise AuthenticationFailed('Authorization 字段是必须的')

        # drf-jwt认证校验算法
        try:
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            raise AuthenticationFailed('签名过期')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('非法用户')
        user = self.authenticate_credentials(payload)
        # 将认证结果丢该drf
        return user, token
