from django.conf.urls import url
from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import YonghuInfo, Authentication, AuthenticationV2
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token


# yonghu_update = YonghuInfo.as_view({
#     'post': 'update'
# })


router = DefaultRouter()
router.register('yonghu_info', YonghuInfo, basename='yonghu_info')             # 获取或更新用户信息
router.register('yonghu_yz', Authentication, basename='yonghu_yz')             # 账号身份认证
router.register('yonghu_yz_new', AuthenticationV2, basename='yonghu_yz_new')   # 新系统账号身份认证


urlpatterns = [
    path('api_login/', obtain_jwt_token),            # jwt认证
    path('api-token-refresh/', refresh_jwt_token),   # jwt刷新
    path('yonghu_logout', views.logout),             # 注销登录
    path('qq_login', views.qq_login),                # QQ登录
] + router.urls