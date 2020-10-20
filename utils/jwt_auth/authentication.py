from datetime import datetime
import datetime as dt
import jwt
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication, jwt_decode_handler
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.utils import jwt_encode_handler

from school import settings
from calendar import timegm
from school.settings import PLATFORM
from yonghu import models
from yonghu import serializers
from rest_framework_jwt.serializers import VerificationBaseSerializer
from rest_framework import serializers as jwt_serializers


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
        'exp': iss_time + api_settings.JWT_EXPIRATION_DELTA,
    }
    if user_data.get("email"):
        payload['email'] = user_data["email"]

    # Include original issued at time for a brand new token,
    # to allow token refresh
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            iss_time.utctimetuple()
        )

    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER
    return payload


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    禁用跨域
    """
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class JSONWebTokenAuthentication(BaseJSONWebTokenAuthentication):

    def get_authorization_header(self, request):
        try:
            auth = request.META.get('HTTP_AUTHORIZATION').split()
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
        token = self.parse_jwt_token(auth)
        if token is None:
            return None
        try:
            # token => payload
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            raise AuthenticationFailed('token已过期')
        except jwt.exceptions:
            raise AuthenticationFailed('非法用户')
        # payload => user
        user = self.authenticate_credentials(payload)
        if user is None:
            return None
        return user, token

    def parse_jwt_token(self, jwt_token):
        """验证jwt前缀是否合法"""
        token = jwt_token.split()
        auth_header_prefix = settings.JWT_AUTH["JWT_AUTH_HEADER_PREFIX"].lower()
        if len(token) != 2 or token[0].lower() != auth_header_prefix:
            return None
        return token[1]


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


class RefreshJwtSerializers(VerificationBaseSerializer):
    """
    刷新token
    """

    def _check_user(self, payload):
        user_id = payload.get("user_id")
        platform = payload.get("platform")
        if not user_id or not platform:
            msg = "Invalid Payload."
            raise jwt_serializers.ValidationError(msg)

        user_model, user_serializer_class = get_platform_user(platform)
        if user_model is None:
            msg = "Invalid Payload."
            raise jwt_serializers.ValidationError(msg)

        try:
            user_obj = user_model.objects.get(id=user_id)
        except user_model.DoesNotExist:
            msg = "Invalid Payload."
            raise jwt_serializers.ValidationError(msg)
        user_serializer = user_serializer_class(user_obj)
        return user_serializer

    def validate(self, attrs):
        token = attrs.get("token")
        payload = self._check_payload(token=token)
        user_serializer = self._check_user(payload)
        platform = payload.get("platform")
        if not platform:
            msg = "Invalid Payload."
            jwt_serializers.ValidationError(msg)
        orig_iat = payload.get('orig_iat')
        if orig_iat:
            # Verify expiration
            refresh_limit = api_settings.JWT_REFRESH_EXPIRATION_DELTA

            if isinstance(refresh_limit, dt.timedelta):
                refresh_limit = (refresh_limit.days * 24 * 3600 +
                                 refresh_limit.seconds)

            expiration_timestamp = orig_iat + int(refresh_limit)
            now_timestamp = timegm(datetime.utcnow().utctimetuple())

            if now_timestamp > expiration_timestamp:
                msg = 'Refresh has expired.'
                raise jwt_serializers.ValidationError(msg)
        else:
            msg = 'orig_iat field is required.'
            raise jwt_serializers.ValidationError(msg)

        new_payload = jwt_payload_handler(user_serializer.data, platform)
        new_payload['orig_iat'] = orig_iat

        return {
            'token': jwt_encode_handler(new_payload),
            'user_data': user_serializer.data
        }
