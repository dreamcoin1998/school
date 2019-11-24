from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import timeTable


router = DefaultRouter()
# router.register('timetable', Timetables, base_name='timetable')  # 获取课表


urlpatterns = [
    path('timetable/', timeTable) # 获取课表
] + router.urls