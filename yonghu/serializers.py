from rest_framework import serializers
from school import settings
from utils.login import code2Session
from .models import QQUser, WXUser, APPUser


class UserCommonSerializers(serializers.ModelSerializer):

    platform = None

    openid = serializers.CharField(required=True, error_messages={'required': "openid 必须存在且必须是string"})
    nickName = serializers.CharField()
    gender = serializers.IntegerField(min_value=0, max_value=2, error_messages={
        "min_value": "gender 可选值为0 1 2，分别代表未知、男、女",
        "max_value": "gender 可选值为0 1 2，分别代表未知、男、女",
    })
    country = serializers.CharField()
    province = serializers.CharField()
    city = serializers.CharField()
    avatarUrl = serializers.URLField()
    is_auth = serializers.BooleanField(read_only=True)
    is_auth_new = serializers.BooleanField(read_only=True)

    @property
    def _get_app_id(self):
        return settings.QQ_APPID

    def _get_openid(self, code, user_info):
        """获取openid
        """
        # 校验参数
        if not isinstance(code, str) and isinstance(user_info, dict):
            error = "code必须是string，user_info必须是dict"
            raise serializers.ValidationError(error)
        res = code2Session.c2s(self._get_app_id, code, platform=self.platform)
        if res.get('errcode') == 0:
            openid = res.get('openid')
            user_info['openid'] = openid
            return user_info
        else:
            error = "后端调用小程序接口获取openid失败"
            raise serializers.ValidationError(error)

    def is_valid(self, raise_exception=False):
        code = self.initial_data.get("code")
        user_info = self.initial_data.get("userInfo")
        try:
            # 将openid加入initial_data方便后续验证
            self.initial_data.update(self._get_openid(code, user_info))
            # 如果已经存在openid则初始化instance
            user_model = getattr(getattr(self, "Meta"), "model")
            user = user_model.objects.filter(pk=user_info["openid"])
            if user.count():
                self.instance = user[0]
        except serializers.ValidationError as exc:
            self._validated_data = {}
            self._errors = exc.detail
            return False
        return super(UserCommonSerializers, self).is_valid()


class empty:
    pass


class QQUserSerializer(UserCommonSerializers):

    platform = "QQ"

    @property
    def _get_app_id(self):
        return settings.QQ_APPID

    class Meta:
        model = QQUser
        fields = ('openid', 'nickName', 'gender', 'country', 'province', 'city', 'avatarUrl', 'is_auth', 'is_auth_new')


class WXUserSerializer(UserCommonSerializers):

    platform = "WX"

    @property
    def _get_app_id(self):
        return settings.WX_APPID

    class Meta:
        model = WXUser
        fields = ('openid', 'nickName', 'gender', 'country', 'province', 'city', 'avatarUrl', 'is_auth', 'is_auth_new')


class APPUserSerializer(UserCommonSerializers):

    platform = "APP"

    class Meta:
        model = APPUser
        fields = ('id', 'email', 'phone', 'nickName', 'gender', 'country', 'province', 'city', 'avatarUrl', 'is_auth', 'is_auth_new')
