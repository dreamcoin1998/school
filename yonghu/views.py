from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UscInfo, NewUSCINFO, QQUser, WXUser, APPUser
from .serializers import QQUserSerializer, WXUserSerializer, APPUserSerializer
from rest_framework import viewsets, mixins
from utils.permissions.permissions import IsOwnerOrReadOnlyInfo
from utils.permissions.permissions import IsAuthenticated
from utils.login import code2Session
from rest_framework.authentication import SessionAuthentication, get_authorization_header
from school import settings
from utils.returnCode.ReturnCode import ReturnCode
from utils.uscSystem.UniversityLogin import UniversityLogin
from utils.uscSystem.UscLogin import UscLogin
from collections import abc
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from rest_framework import serializers


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    禁用跨域
    """
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class QQUserInfo(mixins.UpdateModelMixin, viewsets.ReadOnlyModelViewSet):
    '''
    获取或更新用户信息
    list: http://hostname/auth/yonghu_info/[pk] GET # pk不带获取当前用户，带的话获取指定用户
    update: http://hostname/auth/yonghu_info/pk/ PUT # pk必须带
    '''
    lookup_field = 'pk'
    serializer_class = QQUserSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyInfo)
    authentication_classes = [JSONWebTokenAuthentication, CsrfExemptSessionAuthentication]

    def get_queryset(self):
        try:
            if self.kwargs.get('pk'):
                pk = self.kwargs['pk']
            else:
                pk = self.request.session['pk']
            return QQUser.objects.filter(pk=pk)
        except KeyError:
            return []


class Authentication(mixins.UpdateModelMixin, viewsets.ReadOnlyModelViewSet):
    lookup_field = 'pk'
    serializer_class = QQUserSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyInfo)
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get_queryset(self):
        if self.kwargs.get('pk'):
            pk = self.kwargs['pk']
        else:
            pk = self.request.session['pk']
        return QQUser.objects.filter(pk=pk)

    def update(self, request, *args, **kwargs):
        '''
        用户身份认证
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        user = self.get_object()
        serializer = QQUserSerializer(user)
        # 未验证
        if not user.is_auth:
            # user = request.user.pk
            username = request.data.get('UserName')
            password = request.data.get('Password')
            university = UniversityLogin()
            if university.UscLogin(username, password):
                uscinfo = UscInfo()
                uscinfo.UserName = username
                uscinfo.Password = password
                uscinfo.user = user
                uscinfo.save()
                user.is_auth = True
                user.save()
                return Response(ReturnCode(0, data=serializer.data), status=200)
            else:
                return Response(ReturnCode(1, msg='登录失败'), status=400)
        else:
            return Response(ReturnCode(1, msg='请勿重复验证'), status=status.HTTP_400_BAD_REQUEST)


class AuthenticationV2(Authentication):

    def update(self, request, *args, **kwargs):
        """
        用户身份认证
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user = self.get_object()
        serializer = QQUserSerializer(user)
        # 未验证
        if not user.is_auth_new:
            # user = request.user.pk
            UserName = request.data.get('UserName')
            Password = request.data.get('Password')
            usclogin = UscLogin(UserName, Password)
            if usclogin.UscLoginNew():
                newuscinfo = NewUSCINFO()
                newuscinfo.UserName = UserName
                newuscinfo.Password = Password
                newuscinfo.user = user
                newuscinfo.save()
                user.is_auth_new = True
                user.save()
                return Response(ReturnCode(0, data=serializer.data), status=200)
            else:
                return Response(ReturnCode(1, msg='登录失败'), status=400)
        else:
            return Response(ReturnCode(1, msg='请勿重复验证'), status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["POST"])
def qq_login(request):
    """
    QQ登录
    :param request:
    :return:
    """
    code = request.data.get('code')
    userInfo = request.data.get('userInfo')
    if not isinstance(code, str):
        return Response(ReturnCode(1, msg="code 必须是个str"), status=status.HTTP_400_BAD_REQUEST)
    else:
        res = code2Session.c2s(settings.QQ_APPID, code)
        if res.get('errcode') == 0:
            openid = res.get('openid')
            userInfo['openid'] = openid
            user = QQUser.objects.filter(openid=openid)
            # 不存在,重新创建
            if user.count() == 0:
                serializer = QQUserSerializer(data=userInfo)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(ReturnCode(1, msg=serializer.errors), status=400)
            # 存在,修改
            else:
                serializer = QQUserSerializer(user[0], data=userInfo)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(ReturnCode(1, msg=f'{serializer.errors}'), status=400)
            request.session['pk'] = openid
            return Response(ReturnCode(0, data=serializer.data), status=200)
        return Response(ReturnCode(1, msg='登录失败，请重新登录'), status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["POST"])
def wx_login(request):
    """

    :param request:
    :return:
    """
    code = request.data.get('code')
    userInfo = request.data.get('userInfo')
    if not isinstance(code, str):
        return Response(ReturnCode(1, msg='code 必须是个str'), status=status.HTTP_400_BAD_REQUEST)
    else:
        res = code2Session.c2s(settings.WX_APPID, code, platform='WX')
        if res.get('errcode') == 0:
            openid = res.get('openid')
            userInfo['openid'] = openid
            user = WXUser.objects.filter(openid=openid)
            # 不存在用户
            if user.count() == 0:
                serializer = WXUserSerializer(data=userInfo)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(ReturnCode(1, msg=serializer.errors), status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = WXUserSerializer(user[0], data=userInfo)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(ReturnCode(1, msg=serializer.errors), status=status.HTTP_400_BAD_REQUEST)
            request.session['pk'] = openid
            return Response(ReturnCode(0), status=200)
        return Response(ReturnCode(1, msg='登陆失败'), status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    """小程序登录"""
    permission_classes = []
    authentication_classes = []

    def __init__(self):
        # 所属平台的模型类
        self.user_model = None
        self.user_serializer = None
        self.user_data = None
        self.token = None
        super(LoginAPIView, self).__init__()

    def _user_save(self, app_id=settings.QQ_APPID, platform='QQ'):
        """验证参数可用性并保存用户信息，初始化user_data"""
        code = self.request.data.get('code')
        user_info = self.request.data.get('userInfo')
        # 校验参数
        if not isinstance(code, str) and isinstance(user_info, abc.Mapping):
            return
        res = code2Session.c2s(app_id, code, platform=platform)
        if res.get('errcode') == 0:
            openid = res.get('openid')
            user_info['openid'] = openid
            user = self.user_model.objects.filter(openid=openid)
            # 不存在用户
            if user.count() == 0:
                serializer = self.user_serializer(data=user_info)
                if serializer.is_valid():
                    serializer.save()
                    self.user_data = serializer.data
            else:
                serializer = self.user_serializer(user[0], data=user_info)
                if serializer.is_valid():
                    serializer.save()
                    self.user_data = serializer.data

    def _login(self, platform='QQ'):
        """验证参数可用性并保存用户信息"""
        # 根据不同平台初始化user类型和序列化类型
        if platform == 'QQ':
            self.user_model = QQUser
            self.user_serializer = QQUserSerializer
            self._user_save(app_id=settings.QQ_APPID, platform=platform)
        elif platform == 'WX':
            self.user_model = WXUser
            self.user_serializer = WXUserSerializer
        pass

    def _create_token(self):
        if self.user_data is None:
            payload = jwt_payload_handler(self.user_data)
            token = jwt_encode_handler(payload)
            self.token = token
        raise serializers.ValidationError(detail='user_data为空，参数类型错误或调用接口登陆错误')

    def post(self):
        # 获取登陆平台，默认qq
        platform = self.kwargs.get("platform")
        platform = platform if platform is not None else "qq"
        self._login(platform=platform)
        self._create_token()
        return Response(ReturnCode(0, data=self.user_data, token=self.token))


@csrf_exempt
@api_view()
def logout_view(request):
    """
    用户注销登录
    :param request:
    :return:
    """
    request.session.clear()
    return Response(ReturnCode(0), status=status.HTTP_200_OK)
