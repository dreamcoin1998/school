from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from django.contrib.auth.hashers import make_password
from rest_framework import generics
from django.contrib.auth import get_user_model
from django.shortcuts import render
import re
from django.db.utils import IntegrityError
# from .tasks import random_str, send_register_email
from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import IsAuthenticated
from utils.EmailCode import token_confirm
from utils.permissions import IsOwnerOrReadOnlyInfo
from utils import code2Session
from django.contrib.auth import authenticate, login, logout
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.decorators import action
from rest_framework.authentication import SessionAuthentication
from datetime import datetime
from school import settings
from utils.ReturnCode import ReturnCode
from utils.UniversityLogin import UniversityLogin


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
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyInfo)
    authentication_classes = [JSONWebTokenAuthentication, CsrfExemptSessionAuthentication]

    def get_queryset(self):
        print(self.kwargs.get('pk'))
        if self.kwargs.get('pk'):
            pk = self.kwargs['pk']
        else:
            pk = self.request.user.pk
        return get_user_model().objects.filter(pk=pk)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if user.is_active:
            nickname = request.data.get('nickName')
            if user.change_info(nickname):
                return Response(ReturnCode(0), status=status.HTTP_200_OK)
            else:
                return Response(ReturnCode(1), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(ReturnCode(1), status=status.HTTP_400_BAD_REQUEST)


class Authentication(mixins.UpdateModelMixin, viewsets.ReadOnlyModelViewSet):
    lookup_field = 'pk'
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyInfo)
    authentication_classes = [JSONWebTokenAuthentication, CsrfExemptSessionAuthentication]

    def get_queryset(self):
        print(self.kwargs.get('pk'))
        if self.kwargs.get('pk'):
            pk = self.kwargs['pk']
        else:
            pk = self.request.user.pk
        return get_user_model().objects.filter(pk=pk)

    def update(self, request, *args, **kwargs):
        '''
        用户身份认证
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        user = self.get_object()
        # 未验证
        if not user.is_active:
            user = request.user.pk
            UserName = request.data.get('UserName')
            Password = request.data.get('Password')
            university = UniversityLogin()
            if university.UscLogin(UserName, Password):
                user.is_active = True
                user.save()
                return Response(ReturnCode(0), status=200)
            else:
                return Response(ReturnCode(1, msg='登录失败'), status=400)
        else:
            return Response(ReturnCode(1, msg='请勿重复验证'), status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def qq_login(request):
    '''
    QQ登录
    :param request:
    :return:
    '''
    code = request.data.get('code')
    userInfo = request.data.get('userInfo')
    if type(code) != 'str':
        return Response(ReturnCode(1), status=status.HTTP_400_BAD_REQUEST)
    else:
        res = code2Session.c2s(settings.QQ_APPID, code)
        if res.json().get('errcode') == 0:
            openid = res.json().get('openid')
            userInfo['openid'] = openid
            user = get_user_model().objects.filter(openid=openid)
            ### 不存在,重新创建
            if len(user) == 0:
                serializer = UserSerializer(data=userInfo)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(ReturnCode(1, msg=f'{serializer.errors}'), status=400)
            ### 存在,修改
            else:
                serializer = UserSerializer(user, data=userInfo)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(ReturnCode(1, msg=f'{serializer.errors}'), status=400)
            # 用户登录
            user = authenticate(openid=openid)
            if user is not None:
                login(request, user)
            return Response(ReturnCode(0), status=200)
        else:
            return Response(ReturnCode(1, msg='登录错误，请重新登录'), status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view()
def logout_view(request):
    '''
    用户注销登录
    :param request:
    :return:
    '''
    logout(request)
    return Response(ReturnCode(0), status=status.HTTP_200_OK)