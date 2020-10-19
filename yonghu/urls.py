from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import QQUserInfo, Authentication, AuthenticationV2
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token


# yonghu_update = YonghuInfo.as_view({
#     'post': 'update'
# })


router = DefaultRouter()
router.register('user-info', QQUserInfo, basename='user_info')             # 获取或更新QQ用户信息
router.register('user-auth', Authentication, basename='user_auth')             # 账号身份认证
router.register('user-auth-v2', AuthenticationV2, basename='user_auth_v2')   # 新系统账号身份认证


urlpatterns = [
    path('api-token-refresh/', refresh_jwt_token),   # jwt刷新
    path('login/', views.LoginAPIView.as_view(), name="login"),  # 各平台登录集合
] + router.urls
