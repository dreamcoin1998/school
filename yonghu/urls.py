from django.conf.urls import url
from django.urls import path

from . import views
from rest_framework.routers import DefaultRouter
from .views import YonghuInfo
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token


# yonghu_update = YonghuInfo.as_view({
#     'post': 'update'
# })


router = DefaultRouter()
router.register('yonghu_info', YonghuInfo, base_name='yonghu_info')             # 获取或更新用户信息


urlpatterns = [
    path('api_login/', obtain_jwt_token),            # jwt认证
    path('api-token-refresh/', refresh_jwt_token),   # jwt刷新
    path('yonghu_logout', views.logout),             # 注销登录
    path('qq_login', views.qq_login),                # QQ登录
] + router.urls