from calendar import timegm
from rest_framework_jwt.serializers import VerificationBaseSerializer
from rest_framework import serializers as jwt_serializers
from rest_framework_jwt.utils import jwt_encode_handler
import datetime as dt
from school import settings
from utils.jwt_auth.authentication import get_platform_user, jwt_payload_handler
from datetime import datetime


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
            refresh_limit = settings.JWT_AUTH.get("JWT_REFRESH_EXPIRATION_DELTA")

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
