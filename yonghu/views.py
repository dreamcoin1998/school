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
        print(self.kwargs.get('pk'))
        if self.kwargs.get('pk'):
            pk = self.kwargs['pk']
        else:
            pk = self.request.session['pk']
        return Yonghu.objects.filter(pk=pk)


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
        print('运行')
        return Response(ReturnCode(1, msg="code出错"), status=status.HTTP_400_BAD_REQUEST)
    else:
        res = code2Session.c2s(settings.QQ_APPID, code)
        print(res)
        if res.get('errcode') == 0:
            openid = res.get('openid')
            print('openid: ', openid)
            userInfo['openid'] = openid
            user = Yonghu.objects.filter(openid=openid)
            print(userInfo)
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


# 测试头条小程序前端可用性
@csrf_exempt
@api_view(["POST"])
def testLoginToutiao(request):
    # code = request.data.get('code')
    openid = request.data.get('openid')
    print(openid)
    # anonymous_code = request.data.get('anonymous_code')
    # code2Session.code2sessionToutiao(code)
    return Response(ReturnCode(0))

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


@csrf_exempt
@api_view()
def aaaa(request):
    n = [{'1-2节': [{'Monday': ['安全管理学', '201902769(0)', '蒋复量', '3 4 5 6 8 9 10 11 12 13 14 15', '1-413']}, {'Wednesday': ['安全法规', '201902759(0)', '彭怀德', '7 14', '1-506']}, {'Wednesday': ['机械设计基础B', '201908356(0)', '王湘江', '3 4 5 8 9 10 11 12 13 15 16', '1-404']}]}, {'3-4节': [{'Monday': ['安全人机工程学', '201902785(0)', '王淑云', '4 5 8 9 10 11', '2-207']}, {'Monday': ['大学生创新创业基础', '201904872(0)', '陈代娣', '14', '1-607']}, {'Tuesday': ['安全人机工程学', '201902785(0)', '王淑云', '3 4 5 7 8 9', '9-201']}, {'Tuesday': ['土木工程材料B', '201903769(0)', '王晓峰', '13 14 15 16', '1-509']}, {'Wednesday': ['安全管理学', '201902769(0)', '蒋复量', '5 7 8 9', '1-616']}, {'Wednesday': ['安全人机工程学', '201902785(0)', '王淑云', '10 11 12 13 14', '1-616']}, {'Thursday': ['建筑结构', '201903758(0)', '唐小林', '3 4 5 7 8 9 10 11 12 13 14 15 16', '1-602']}, {'Friday': ['安全系统工程', '201902789(0)', '叶勇军', '4 5 8 9 10 11 12 13', '1-614']}, {'Friday': ['电气安全工程', '201902791(0)', '汪弘', '14 15', '1-614']}, {'Friday': ['数据结构Ⅰ', '201907968(0)', '龚向坚', '8 9 10 11 12 13 14 15 16 17', '1-602']}]}, {'5-6节': [{'Monday': ['建筑结构', '201903758(0)', '唐小林', '3 4 5 6 8 9 10 11 12 13 14', '1-108']}, {'Tuesday': ['软件设计模式', '201906981(0)', '蒋良卫', '3 4 5 7 8 9 10 11 12 13 14 15', '8-409']}, {'Tuesday': ['机械设计基础B', '201908356(0)', '王湘江', '9 10 11 12 13 14 15', '1-103']}, {'Wednesday': ['土木工程材料B', '201903769(0)', '王晓峰', '3 4 9 10 11 13 14 15 16', '1-507']}, {'Thursday': ['大学生创新创业基础', '201904872(0)', '陈代娣', '3 4 5 7 8 9 10 11 12 13 14 15 16', '2-303']}, {'Friday': ['机械设计基础B', '201908356(0)', '王湘江', '5 9 10 11 13 14 15 16', '1-207']}]}, {'7-8节': [{'Monday': ['安全法规', '201902759(0)', '彭怀德', '3 6 13 14', '1-406']}, {'Monday': ['土木工程材料B', '201903769(0)', '王晓峰', '4 5 8 9 10 11 12', '1-412']}, {'Tuesday': ['安全系统工程', '201902789(0)', '叶勇军', '3 4 5 7 8 9 10 11 12 13 14 15', '1-414']}, {'Wednesday': ['安全法规', '201902759(0)', '彭怀德', '3 4 5 7 8 14', '1-113']}, {'Wednesday': ['大学生创新创业基础', '201904872(0)', '陈代娣', '15 16', '2-203']}, {'Thursday': ['电气安全工程', '201902791(0)', '汪弘', '3 4 5 7 8 9 10 11 12 13 14 15', '1-616']}]}, {'9-10节': [{'Monday': ['★数据结构Ⅰ实验', '201906362(0)', '曹军', '8 9 10 11 12 13 14 15 16 17 18', '8-601-A']}, {'Tuesday': ['数据结构Ⅰ', '201907968(0)', '龚向坚', '7 8 9 10 11', '8-508']}, {'Wednesday': ['★数据结构Ⅰ实验', '201906362(0)', '曹军', '13 14 15 16 17', '8-601-A']}, {'Thursday': ['数据结构Ⅰ', '201907968(0)', '龚向坚', '7 8 9 10 11 12 13 14 15', '8-310']}]}]
    return Response(ReturnCode(0, data=n), status=200)

@csrf_exempt
@api_view()
def bbbb(request):
    n = [{'1一2节': [{'Monday': ['大学生职业发展与就业指导2', 'none', '廖大琪讲师（高校）', '14 15 16 17 18', '1-511']}]}, {'3一4节': [{'Wednesday': ['建筑安全工程', 'none', '杨蓉讲师（高校）', '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15', '1-603']}]}, {'5一6节': [{'Monday': ['防火防爆技术', 'none', '钟永明高级工程师', '3 4 5 6 7 8 9 10 11 12 13 14 15', '1-413']}, {'Monday': ['职业卫生与防护', 'none', '黄萍萍讲师（高校）', '1 2', '1-203']}, {'Wednesday': ['职业卫生与防护', 'none', '黄萍萍讲师（高校）', '2 3 4 5 6 7 8 9 10 11 12 13 14 15', '1-515']}, {'Friday': ['建筑安全工程', 'none', '杨蓉讲师（高校）', '12 13 14 15', '1-603']}]}, {'7一8节': [{'Monday': ['地下工程安全技术', 'none', '兰明', '1 2', '1-215']}, {'Wednesday': ['地下工程安全技术', 'none', '兰明', '2 3 4 5 6 7 8 9 10 11 12 13 14 15', '1-603']}, {'Thursday': ['安全检测与监控技术', 'none', '余修武教授', '1 2 3 4 8 9 10 11 12 13 14', '1-414']}]}, {'9一10节': []}, {'11一12节': []}]
    return Response(ReturnCode(0, data=n), status=200)