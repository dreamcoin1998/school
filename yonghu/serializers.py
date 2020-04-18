from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Yonghu
from django.contrib.auth import get_user_model


class YonghuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Yonghu
        fields = ('openid', 'nickName', 'gender', 'country', 'province', 'city', 'avatarUrl', 'is_auth', 'is_auth_new')