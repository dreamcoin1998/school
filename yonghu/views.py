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
# from .models import VerifyCode
from datetime import datetime
from school import settings


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
    queryset = get_user_model().objects.all()
    lookup_field = 'pk'
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyInfo)
    authentication_classes = [JSONWebTokenAuthentication, CsrfExemptSessionAuthentication]

    def get_queryset(self):
        print(self.kwargs.get('pk'))
        if self.kwargs.get('pk'):
            pk = int(self.kwargs['pk'])
        else:
            pk = self.request.user.id
        return get_user_model().objects.filter(pk=pk)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if user.is_active:
            nickname = request.data.get('nickname')
            info = request.data.get('info')
            if user.change_info(nickname, info):
                return Response({'msg': '修改成功', 'code': '0'}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': '昵称已存在', 'code': '1'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg': '账号未激活，请激活后再试。', 'code': '2'}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET'])
def qq_login(request):
    code = request.data.get('code')
    userInfo = request.data.get('userInfo')
    data = {}
    if type(code) != 'str':
        data['code'] = 0
        data['msg'] = 'code格式错误'
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    else:
        res = code2Session.c2s(settings.QQ_APPID, code)
        if res.json().get('errcode') == 0:
            openid = res.json().get('openid')
            # session_key = res.json().get('session_key')
            nickName = userInfo.get('nickName')
            avatarUrl = userInfo.get('avatarUrl')
            gender = userInfo.get('gender')
            country = userInfo.get('country')
            province = userInfo.get('province')
            city = userInfo.get('city')

        else:
            data['code'] = 1
            data['msg'] = '登录错误，请重新登录'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
def yonghu_login(request):
    '''
    用户账号登录
    :param request:
    :return:
    '''
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({'msg': '登陆成功', 'code': '0'}, status=status.HTTP_200_OK)
    else:
        return Response({'msg': '用户名或密码错误', 'code': '1'}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view()
def logout_view(request):
    '''
    用户注销登录
    :param request:
    :return:
    '''
    logout(request)
    return Response({'msg': '注销成功', 'code': 0}, status=status.HTTP_200_OK)


# @csrf_exempt
# @api_view(['POST'])
# def email_code(request):
#     '''
#     邮箱登录验证码
#     :param request:
#     :return:
#     '''
#     email = request.data.get('email')
#     send_type = request.data.get('send_type')
#     if not get_user_model().objects.filter(email=email):
#         return Response({'msg': '当前邮箱未关联用户', 'code': '1'}, status=status.HTTP_400_BAD_REQUEST)
#     send_register_email.delay(email, send_type=send_type)
#     return Response({'msg': '验证码发送成功', 'code': '0'}, status=status.HTTP_200_OK)


# @csrf_exempt
# @api_view(['POST'])
# def email_login(request):
#     '''
#     邮箱登录
#     :param request:
#     :return:
#     '''
#     email = request.data.get('email')
#     code = request.data.get('code')
#     if not get_user_model().objects.filter(email=email):
#         return Response({'msg': '当前邮箱未关联用户', 'code': '1'}, status=status.HTTP_400_BAD_REQUEST)
#     verifycode = VerifyCode.objects.filter(email=email, code=code, send_type='email_login')
#     if verifycode:
#         dt = verifycode[0].send_time
#         if is_overdue(dt):
#             user = get_user_model().objects.get(email=email)
#             login(request, user)
#             return Response({'msg': '登陆成功', 'code': '0'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'msg': '验证码超时', 'code': '2'}, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response({'msg': '验证码错误', 'code': '3'}, status=status.HTTP_400_BAD_REQUEST)


class UpdataPassword(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    '''
    更改密码
    '''
    lookup_field = 'pk'
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyInfo)
    authentication_classes = [JSONWebTokenAuthentication, CsrfExemptSessionAuthentication]
    def get_queryset(self):
        return get_user_model().objects.filter(pk=self.request.user.id)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        old_passwd = request.data.get('old_passwd')
        new_passwd = request.data.get('new_passwd')
        if user.is_active:
            if user.check_password(old_passwd):
                user.password = make_password(new_passwd)
                user.save()
                return Response({'msg': '密码修改成功', 'code': 0}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': '密码错误', 'code': 1}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg': '账号未激活', 'code': 1})


# class UpdateEmail(mixins.UpdateModelMixin, viewsets.GenericViewSet):
#     '''
#     修改认证邮箱
#     '''
#     lookup_field = 'pk'
#     serializer_class = UserSerializer
#     permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyInfo)
#     authentication_classes = [JSONWebTokenAuthentication, CsrfExemptSessionAuthentication]
#     def get_queryset(self):
#         return get_user_model().objects.filter(pk=self.request.user.id)
#
#     def update(self, request, *args, **kwargs):
#         user = self.get_object()
#         email = request.data.get('email')
#         code = request.data.get('email')
#         if user.is_active:
#             verifycode = VerifyCode.objects.filter(email=email, code=code, send_type='update_email')
#             if verifycode:
#                 dt = verifycode[0].send_time
#                 if is_overdue(dt):
#                     user.email = email
#                     user.save()
#                     return Response({'msg': '邮箱重置成功', 'code': '0'}, status=status.HTTP_200_OK)
#                 else:
#                     return Response({'msg': '验证码超时', 'code': 1}, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 return Response({'msg': '验证码错误', 'code': 1}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({'msg': '账号未激活', 'code': 1}, status=status.HTTP_400_BAD_REQUEST)


# class FindPasswordByEmail(generics.UpdateAPIView):
#     '''
#     通过验证邮箱重置密码
#     '''
#     queryset = get_user_model().objects.all()
#     serializer_class = UserSerializer
#
#     @action(methods=['PUT', 'POST'], detail=False)
#     def update(self, request, *args, **kwargs):
#         email = request.data.get('email')
#         code = request.data.get('code')
#         new_passwd = request.data.get('new_passwd')
#         user = get_user_model().objects.filter(email=email)
#         if not user:
#             return Response({'msg': '当前邮箱未关联用户', 'code': 1}, status=status.HTTP_400_BAD_REQUEST)
#         verifycode = VerifyCode.objects.filter(email=email, code=code, send_type='forget')
#         if user[0].is_active:
#             if verifycode:
#                 dt = verifycode[0].send_time
#                 if is_overdue(dt):
#                     user[0].set_password(new_passwd)
#                     user[0].save()
#                     return Response({'msg': '密码重置成功', 'code': '0'}, status=status.HTTP_200_OK)
#                 else:
#                     return Response({'msg': '验证码超时', 'code': 1}, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 return Response({'msg': '验证码错误', 'code': 1}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({'msg': '账号未激活', 'code': 1}, status=status.HTTP_400_BAD_REQUEST)

def is_overdue(time):
    '''
    检查验证码是否过期
    :param time:
    :return:
    '''
    deltertime = int(datetime.now().timestamp()) - int(time.timestamp())
    return deltertime <= 300


# @csrf_exempt
# @api_view(['GET', 'PUT'])
# def Yonghu_info(request):
#     """
#     获取yonghu信息。
#     """
#     try:
#         pk = request.query_params.get('pk')
#         yonghu = get_user_model().objects.get(pk=pk)
#     except User.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     # 获取用户信息
#     if request.method == 'GET':
#         print(request.session.get('userID'))
#         serializer = UserSerializer(yonghu)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# @csrf_exempt
# @api_view(['POST'])
# def yonghu_create(request):
#     """
#     注册
#     """
#     if request.method == 'POST':
#         username = request.data.get('username')
#         phone = request.data.get('phone')
#         email = request.data.get('email')
#         password = request.data.get('password')
#         ### 账号密码合法性验证
#         if password is None or username is None:
#             return Response({'msg': '账号或密码为空', 'code': '1'}, status=status.HTTP_400_BAD_REQUEST)
#         s = re.match(r"[0-9a-zA-Z]+", username)
#         if s is None:
#             return Response({'msg': '账号不合法', 'code': '2'}, status=status.HTTP_400_BAD_REQUEST)
#         if len(s.group()) != len(username):
#             print(s.group())
#             return Response({'msg': '账号不合法', 'code': '2'}, status=status.HTTP_400_BAD_REQUEST)
#         ### 验证邮箱和手机号是否重复
#         if phone is None and email is None:
#             return Response({'msg': '邮箱和手机号至少要有一个', 'code': '3'}, status=status.HTTP_400_BAD_REQUEST)
#         if email is not None:
#             user = get_user_model().objects.filter(email=email)
#             if user:
#                 return Response({'msg': '邮箱已验证过', 'code': '4'}, status=status.HTTP_400_BAD_REQUEST)
#         if phone is not None:
#             user = get_user_model().objects.filter(phone=phone)
#             if user:
#                 return Response({'msg': '手机号已验证过', 'code': '5'}, status=status.HTTP_400_BAD_REQUEST)
#             print(get_user_model().objects.filter(username=username))
#         if len(get_user_model().objects.filter(username=username)) == 0:
#             try:
#                 get_user_model().objects.create(
#                     username = username,
#                     phone = phone,
#                     email = email,
#                     password = make_password(password),
#                     nickname = random_str() ### 创建随机昵称
#                 )
#                 token = token_confirm.generate_validate_token(username)
#                 send_register_email.delay(email=email,username=username,token=token,send_type="register")
#                 return Response({'msg': '注册成功，', 'code': '0'}, status=status.HTTP_200_OK)
#             except IntegrityError as e:
#                 print(e)
#                 return Response({'msg': '注册失败,请重新注册', 'code': '7'}, status=status.HTTP_400_BAD_REQUEST)
#         return Response({'msg': '账号已存在', 'code': '6'}, status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt
# @api_view(['GET'])
# def email_test(request):
#     '''
#     邮箱可用性验证测试
#     :param request:
#     :return:
#     '''
#     user = get_user_model().objects.get(username='15259695263')
#     send_register_email.delay(email=user.email, username=user.username, token=token_confirm.generate_validate_token(user.username), send_type="register")
#     return Response({'msg': 'success.'}, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
def active_email(request):
    '''
    通过邮箱激活验证
    :param request:
    :return:
    '''
    token = request.query_params.get('token')
    try:
        username = token_confirm.confirm_validate_token(token) # 将用户名解析出来
    except Exception:
        username = token_confirm.remove_validate_token(token) # 过期，则将用户名解析出来
        users = get_user_model().objects.filter(username=username)
        for user in users:
            # 验证过期
            if user.is_active == False:
                user.delete() # 删除用户
                # msg = {'message': '验证已过期，请重新注册'}
                return Response('验证已过期')
            # 已经验证过
            else:
                return Response('已经验证过')
    try:
        user = get_user_model().objects.get(username=username)
        if user.is_active == True:
            return Response('已经验证过')
    except Exception as e:
        print(e)
        return Response('您验证过的用户不存在!')
    user.is_active = True
    user.save()
    return Response('验证成功!')