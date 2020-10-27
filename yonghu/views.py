from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UscInfo, NewUSCINFO, QQUser
from .serializers import QQUserSerializer
from rest_framework import viewsets, mixins
from utils.permissions.permissions import IsOwnerOrReadOnlyInfo
from utils.permissions.permissions import IsAuthenticated
from utils.returnCode import ReturnCode
from utils.uscSystem.UniversityLogin import UniversityLogin
from utils.uscSystem.UscLogin import UscLogin
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler, jwt_decode_handler
from utils.jwt_auth.authentication import JSONWebTokenAuthentication, CsrfExemptSessionAuthentication
from utils.jwt_auth.authentication import get_platform_user, parse_jwt_token
from rest_framework_jwt.views import JSONWebTokenAPIView
from utils.jwt_auth.serializers import RefreshJwtSerializers


class GetOrUpdateUserInfo(mixins.UpdateModelMixin, viewsets.ReadOnlyModelViewSet):
    """
    获取或更新用户信息
    list: http://hostname/auth/yonghu_info/[pk] GET # pk不带获取当前用户，带的话获取指定用户
    update: http://hostname/auth/yonghu_info/pk/ PUT # pk必须带
    """
    # lookup_field = "pk"
    serializer_class = None
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyInfo)
    authentication_classes = [JSONWebTokenAuthentication, CsrfExemptSessionAuthentication]

    def get_queryset(self):
        user = self.request.user
        if user is None:
            return []
        return user

    def initial_serializer(self):
        # 获取token，从token获取platform
        token = self.request.auth
        payload = jwt_decode_handler(token)
        platform = payload.get("platform")
        _, user_serializer = get_platform_user(platform)
        # 初始化serializer
        self.serializer_class = user_serializer

    def list(self, request, *args, **kwargs):
        # 初始化serializer_class
        self.initial_serializer()
        user_obj = request.user
        serializer = self.get_serializer(user_obj)
        return Response(ReturnCode.ResponseCode(data=serializer.data))

    def update(self, request, *args, **kwargs):
        # 初始化serializer_class
        self.initial_serializer()
        user_obj = request.user
        serializer = self.get_serializer(data=user_obj)
        if serializer.is_valid():
            serializer.save()
            return Response(ReturnCode.ResponseCode(data=serializer.validated_data))
        return Response(ReturnCode.UpdateUserInfoFailResponse(msg=serializer.errors))


class Authentication(mixins.UpdateModelMixin, viewsets.ReadOnlyModelViewSet):
    """教务系统登录验证"""

    lookup_field = 'pk'
    serializer_class = QQUserSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyInfo)
    authentication_classes = [CsrfExemptSessionAuthentication]
    usc_info_class = UscInfo
    usc_login_class = UniversityLogin

    def get_queryset(self):
        if self.kwargs.get('pk'):
            pk = self.kwargs['pk']
        else:
            pk = self.request.session.get('pk')
        return QQUser.objects.filter(pk=pk)

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
        if not user.is_auth:
            username = request.data.get('UserName')
            password = request.data.get('Password')
            usc_login_obj = self.usc_login_class(username, password)
            if usc_login_obj.usc_login():
                usc_info = self.usc_info_class()
                usc_info.UserName = username
                usc_info.Password = password
                usc_info.user = user
                usc_info.save()
                user.is_auth = True
                user.save()
                return Response(ReturnCode.ResponseCode(data=serializer.data), status=200)
            else:
                return Response(ReturnCode.AuthenticateErrorResponse(), status=400)
        else:
            return Response(ReturnCode.ReAuthErrorResponse(), status=400)


class AuthenticationV2(Authentication):
    """使用新教务系统验证"""
    usc_info_class = NewUSCINFO
    usc_login_class = UscLogin
    versioning_class = "v2.0"


class LoginAPIView(APIView):
    """登录类 使用token验证"""
    permission_classes = []
    authentication_classes = []

    def __init__(self):
        # 所属平台的模型类
        self.user_model = None
        self.user_serializer = None
        self.user_data = None
        self.token = None
        super(LoginAPIView, self).__init__()

    def _get_user_class_info(self):
        # 根据不同平台初始化user类型和序列化类型
        user_model, user_serializer = get_platform_user(platform=self.platform)
        return user_model, user_serializer

    def _create_token(self):
        # user_data非空登陆成功，为空说明登陆失败
        if self.user_data is not None:
            payload = jwt_payload_handler(self.user_data, self.platform)
            token = jwt_encode_handler(payload)
            self.token = token
        else:
            self.error = 'user_data为空，platform传入错误' if self.error is None else self.error
            self.status_code = 400

    def post(self, request):
        platform = request.query_params.get("platform")
        self.platform = platform if platform is not None else self.platform
        user_model, user_serializer = self._get_user_class_info()
        serializer = user_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            self.user_data = serializer.data
        else:
            return Response(ReturnCode.LoginFailResponse(msg=serializer.errors), status=400)
        self._create_token()
        if self.user_data is None or self.token is None:
            return Response(ReturnCode.LoginFailResponse(msg=self.error), status=self.status_code)
        return Response(ReturnCode.ResponseCode(data=self.user_data, token=self.token), status=200)


class RefreshJSONWebToken(JSONWebTokenAPIView):
    serializer_class = RefreshJwtSerializers
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            user_data = serializer.object.get("user_data")
            token = serializer.object.get("token")
            return Response(ReturnCode.ResponseCode(data=user_data, token=token))
        return Response(ReturnCode.TokenRefreshExpiredResponse(msg=serializer.errors), status=400)


@csrf_exempt
@api_view()
def logout_view(request):
    """
    用户注销登录
    :param request:
    :return:
    """
    request.session.clear()
    return Response(ReturnCode.ResponseCode(), status=status.HTTP_200_OK)
