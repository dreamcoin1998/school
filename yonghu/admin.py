from django.contrib import admin
from .models import User, UscInfo

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('openid', 'nickName', 'gender', 'country', 'province', 'city', 'avatarUrl', 'is_active')


@admin.register(UscInfo)
class UscInfoAdmin(admin.ModelAdmin):
    list_display = ('UserName', 'user')

# @admin.register(VerifyCode)
# class VerifyCode(admin.ModelAdmin):
#     list_display = ('code', 'email', 'send_type', 'send_time')