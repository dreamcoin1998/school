from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('forum/', include('forum.urls')),
    path('transaction/', include('transaction.urls')), # 二手交易模块
    path('auth/', include('yonghu.urls')),             # 登陆验证模块
    path('api/', include('tools.urls')),
    path('images/', include('images.urls')),
    path('feedback/', include('feedback.urls'))        # 用户反馈
]