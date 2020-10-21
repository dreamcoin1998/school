from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import QQUserInfo, Authentication, AuthenticationV2


# yonghu_update = YonghuInfo.as_view({
#     'post': 'update'
# })


router = DefaultRouter()
router.register('user-info', QQUserInfo, basename='user_info')             # 获取或更新QQ用户信息
router.register('user-auth', Authentication, basename='user_auth')             # 账号身份认证
router.register('user-auth-v2', AuthenticationV2, basename='user_auth_v2')   # 新系统账号身份认证


urlpatterns = [
    path('api-token-refresh/', views.RefreshJSONWebToken.as_view()),   # jwt刷新
    path('api-token-auth/', views.LoginAPIView.as_view(), name="login"),  # 各平台登录接口
] + router.urls
