from django.contrib import admin
from .models import QQUser, UscInfo, NewUSCINFO, WXUser, APPUser


@admin.register(QQUser)
class QQUserAdmin(admin.ModelAdmin):
    list_display = ('openid', 'nickName', 'gender', 'country', 'province', 'city', 'avatarUrl', 'is_auth', 'is_auth_new')


@admin.register(WXUser)
class WXUserAdmin(admin.ModelAdmin):
    list_display = ('openid', 'nickName', 'gender', 'country', 'province', 'city', 'avatarUrl', 'is_auth', 'is_auth_new')


@admin.register(APPUser)
class APPUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone', 'nickName', 'gender', 'country', 'province', 'city', 'avatarUrl', 'is_auth', 'is_auth_new')


@admin.register(UscInfo)
class UscInfoAdmin(admin.ModelAdmin):
    list_display = ('UserName', 'QQUser', 'WXUser', 'APPUser')


@admin.register(NewUSCINFO)
class NewUSCINFOAdmin(admin.ModelAdmin):
    list_display = ('UserName', 'QQUser', 'WXUser', 'APPUser')
