from rest_framework import serializers
from django.contrib.auth.models import User
from .models import User
from django.contrib.auth import get_user_model


### 用户序列化类
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('openid', 'nickName', 'gender', 'country', 'province', 'city', 'avatarUrl', 'is_auth')


### 验证码序列化类
# class VerifyCodeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = VerifyCode
#         fields = ('id', 'code', 'email', 'send_type', 'send_time')