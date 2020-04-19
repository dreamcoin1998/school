from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('forum/', include('forum.urls')),
    path('transaction/', include('transaction.urls')), # 二手交易模块
    path('auth/', include('yonghu.urls')),             # 登陆验证模块
    path('api/', include('tools.urls')),
    path('images/', include('images.urls')),
    path('feedback/', include('feedback.urls')),       # 用户反馈
<<<<<<< HEAD
    path('messages/', include('Messages.urls')),         # 留言模块
=======
    path('messages/', include('Messages.urls')),       # 留言模块
>>>>>>> 4eb7845025e61927b367367ab0ac8117faf53c48
]