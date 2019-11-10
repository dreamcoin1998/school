from django.conf.urls import url
from django.urls import path

from . import views
from rest_framework.routers import DefaultRouter
from .views import YonghuInfo, UpdataPassword
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token


# yonghu_update = YonghuInfo.as_view({
#     'post': 'update'
# })


router = DefaultRouter()
router.register('yonghu_info', YonghuInfo, base_name='yonghu_info')             # 获取或更新用户信息
router.register('update_password', UpdataPassword, base_name='updata_password') # 修改密码
# router.register('update_email', UpdateEmail, base_name='update_email')          # 修改认证邮箱


urlpatterns = [
    path('api_login/', obtain_jwt_token),            # jwt认证
    path('api-token-refresh/', refresh_jwt_token),   # jwt刷新
    # path('yonghu_create/', views.yonghu_create),     # 用户注册
    path('activate/', views.active_email),           # 用户激活
    path('yonghu_login/', views.yonghu_login),       # 账号登录
    # path('email_code/', views.email_code),           # 发送验证码
    # path('email_login/', views.email_login),         # 邮箱登录
    path('yonghu_logout', views.logout),             # 注销登录
    # path('find_passwd_by_email/', views.FindPasswordByEmail.as_view()), # 通过邮箱找回密码
] + router.urls