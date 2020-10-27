from datetime import datetime
import jwt
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication, jwt_decode_handler
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import SessionAuthentication
from school import settings
from calendar import timegm
from school.settings import PLATFORM
from yonghu import models
from yonghu import serializers


def jwt_payload_handler(user_data, platform):
    if user_data.get("openid"):
        user_id = user_data["openid"]
    else:
        user_id = user_data["id"]
    iss_time = datetime.utcnow()
    payload = {
        "user_id": user_id,
        "nickname": user_data["nickName"],
        "platform": platform,
        'exp': iss_time + settings.JWT_AUTH.get("JWT_EXPIRATION_DELTA"),
    }
    if user_data.get("email"):
        payload['email'] = user_data["email"]

    # Include original issued at time for a brand new token,
    # to allow token refresh
    if settings.JWT_AUTH.get("JWT_ALLOW_REFRESH"):
        payload['orig_iat'] = timegm(
            iss_time.utctimetuple()
        )

    if settings.JWT_AUTH.get("JWT_AUDIENCE") is not None:
        payload['aud'] = settings.JWT_AUTH.get("JWT_AUDIENCE")

    if settings.JWT_AUTH.get("JWT_ISSUER") is not None:
        payload['iss'] = settings.JWT_AUTH.get("JWT_ISSUER")
    return payload


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    禁用跨域
    """
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


def parse_jwt_token(jwt_token):
    """验证jwt前缀是否合法"""
    token = jwt_token.split(" ")
    auth_header_prefix = settings.JWT_AUTH["JWT_AUTH_HEADER_PREFIX"].lower()
    if len(token) != 2 or token[0].lower() != auth_header_prefix:
        return None
    return token[1]


class JSONWebTokenAuthentication(BaseJSONWebTokenAuthentication):
    """JWT验证"""
    def get_authorization_header(self, request):
        try:
            auth = request.META.get('HTTP_AUTHORIZATION')
            return auth
        except AttributeError as e:
            return None

    def authenticate_credentials(self, payload):
        try:
            user_id = payload["user_id"]
            platform = payload["platform"]
        except KeyError as e:
            return None
        user_model, _ = get_platform_user(platform=platform)
        if user_model is None:
            return None
        user = user_model.objects.filter(pk=user_id)
        if user.count() == 0:
            return None
        return user[0]

    def authenticate(self, request):
        auth = self.get_authorization_header(request)
        if auth is None:
            return None
        # 自定义校验规则：auth_header_prefix token
        token = parse_jwt_token(auth)
        if token is None:
            return None
        try:
            # token => payload
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            raise AuthenticationFailed('token已过期')
        except jwt.exceptions.DecodeError:
            raise AuthenticationFailed('非法用户')
        # payload => user
        user = self.authenticate_credentials(payload)
        if user is None:
            return None
        return user, token


def get_platform_user(platform):
    try:
        platform = platform if platform else settings.DEFAULT_PLATFORM
        user_model_class_name = PLATFORM[platform]["model"]
        user_serializer_class_name = PLATFORM[platform]["serializer"]
    except KeyError:
        return None, None
    if hasattr(models, user_model_class_name):
        user_model = getattr(models, user_model_class_name)
    else:
        raise AttributeError("yonghu.model里面没有 %s 类" % user_model_class_name)
    if hasattr(serializers, user_serializer_class_name):
        user_serializer = getattr(serializers, user_serializer_class_name)
    else:
        raise AttributeError("yonghu.serializers里面没有 %s 类" % user_serializer_class_name)
    return user_model, user_serializer
