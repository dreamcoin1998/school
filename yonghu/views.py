from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UscInfo, Yonghu, NewUSCINFO
from .serializers import YonghuSerializer
from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins, generics
from utils.permissions import IsOwnerOrReadOnlyInfo
from utils.permissions import IsAuthenticated
from utils import code2Session
from django.contrib.auth import authenticate, login, logout
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from school import settings
from utils.ReturnCode import ReturnCode
from utils.UniversityLogin import UniversityLogin
from django.contrib.auth.backends import ModelBackend
from utils.UscLogin import UscLogin


class MyYonghuBackend(ModelBackend):
    '''
    自定义登陆验证
    '''
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            openid = kwargs['pk']
            user = Yonghu.objects.get(openid=openid)
            return user
        except Exception as e:
            return None


class CsrfExemptSessionAuthentication(SessionAuthentication):
    '''
    禁用跨域
    '''
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class YonghuInfo(mixins.UpdateModelMixin, viewsets.ReadOnlyModelViewSet):
    '''
    获取或更新用户信息
    list: http://hostname/auth/yonghu_info/[pk] GET # pk不带获取当前用户，带的话获取指定用户
    update: http://hostname/auth/yonghu_info/pk/ PUT # pk必须带
    '''
    lookup_field = 'pk'
    serializer_class = YonghuSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyInfo)
    authentication_classes = [JSONWebTokenAuthentication, CsrfExemptSessionAuthentication]

    def get_queryset(self):
        try:
            # print(self.kwargs.get('pk'))
            if self.kwargs.get('pk'):
                pk = self.kwargs['pk']
            else:
                pk = self.request.session['pk']
            return Yonghu.objects.filter(pk=pk)
        except KeyError:
            return []


class Authentication(mixins.UpdateModelMixin, viewsets.ReadOnlyModelViewSet):
    lookup_field = 'pk'
    serializer_class = YonghuSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyInfo)
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get_queryset(self):
        print(self.kwargs.get('pk'))
        if self.kwargs.get('pk'):
            pk = self.kwargs['pk']
        else:
            pk = self.request.session['pk']
            print("user:", self.request.user)
        return Yonghu.objects.filter(pk=pk)

    def update(self, request, *args, **kwargs):
        '''
        用户身份认证
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        user = self.get_object()
        serializer = YonghuSerializer(user)
        # 未验证
        if not user.is_auth:
            # user = request.user.pk
            UserName = request.data.get('UserName')
            Password = request.data.get('Password')
            university = UniversityLogin()
            if university.UscLogin(UserName, Password):
                uscinfo = UscInfo()
                uscinfo.UserName = UserName
                uscinfo.Password = Password
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
        '''
        用户身份认证
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        user = self.get_object()
        serializer = YonghuSerializer(user)
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
    '''
    QQ登录
    :param request:
    :return:
    '''
    code = request.data.get('code')
    # print(type(code))
    userInfo = request.data.get('userInfo')
    if type(code) != type('str'):
        # print('运行')
        return Response(ReturnCode(1, msg="code出错"), status=status.HTTP_400_BAD_REQUEST)
    else:
        res = code2Session.c2s(settings.QQ_APPID, code)
        # print(res)
        if res.get('errcode') == 0:
            openid = res.get('openid')
            # print('openid: ', openid)
            userInfo['openid'] = openid
            user = Yonghu.objects.filter(openid=openid)
            # print(userInfo)
            ### 不存在,重新创建
            if len(user) == 0:
                serializer = YonghuSerializer(data=userInfo)
                print(serializer.is_valid())
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(ReturnCode(1, msg=serializer.errors), status=400)
            ### 存在,修改
            else:
                serializer = YonghuSerializer(user[0], data=userInfo)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(ReturnCode(1, msg=f'{serializer.errors}'), status=400)
            request.session['pk'] = openid
            return Response(ReturnCode(0, data=serializer.data), status=200)
        return Response(ReturnCode(1, msg='登录失败，请重新登录'), status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view()
def logout_view(request):
    '''
    用户注销登录
    :param request:
    :return:
    '''
    request.session.clear()
    return Response(ReturnCode(0), status=status.HTTP_200_OK)