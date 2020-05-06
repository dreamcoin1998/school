from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import timeTable, getTimetable, check_score


router = DefaultRouter()
# router.register('uscSystem', Timetables, base_name='uscSystem')  # 获取课表


urlpatterns = [
    path('uscSystem/', timeTable),        # 获取课表
    path('newtimeTable/', getTimetable),  # 新教务在线获取课表
    path('score/', check_score),          # 查询成绩
] + router.urls