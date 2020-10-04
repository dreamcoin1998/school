from rest_framework import serializers
from .models import QQUser, WXUser, APPUser


class QQUserSerializer(serializers.ModelSerializer):

    openid = serializers.CharField(required=True, error_messages="openid 必须存在且必须是string")
    nickName = serializers.CharField()
    gender = serializers.IntegerField(min_value=0, max_value=2, error_messages="gender 可选值为0 1 2，分别代表未知、男、女")
    country = serializers.CharField()
    province = serializers.CharField()
    city = serializers.CharField()
    avatarUrl = serializers.URLField()
    is_auth = serializers.BooleanField()
    is_auth_new = serializers.BooleanField()

    class Meta:
        model = QQUser


class WXUserSerializer(serializers.ModelSerializer):

    openid = serializers.CharField(required=True, error_messages="openid 必须存在且必须是string")
    nickName = serializers.CharField()
    gender = serializers.IntegerField(min_value=0, max_value=2, error_messages="gender 可选值为0 1 2，分别代表未知、男、女")
    country = serializers.CharField()
    province = serializers.CharField()
    city = serializers.CharField()
    avatarUrl = serializers.URLField()
    is_auth = serializers.BooleanField()
    is_auth_new = serializers.BooleanField()

    class Meta:
        model = WXUser
        fields = ('openid', 'nickName', 'gender', 'country', 'province', 'city', 'avatarUrl', 'is_auth', 'is_auth_new')


class APPUserSerializer(serializers.ModelSerializer):

    openid = serializers.CharField(required=True, error_messages="openid 必须存在且必须是string")
    nickName = serializers.CharField()
    gender = serializers.IntegerField(min_value=0, max_value=2, error_messages="gender 可选值为0 1 2，分别代表未知、男、女")
    country = serializers.CharField()
    province = serializers.CharField()
    city = serializers.CharField()
    avatarUrl = serializers.URLField()
    is_auth = serializers.BooleanField()
    is_auth_new = serializers.BooleanField()

    class Meta:
        model = APPUser
        fields = ('id', 'email', 'phone', 'nickName', 'gender', 'country', 'province', 'city', 'avatarUrl', 'is_auth', 'is_auth_new')
