from django.contrib import admin
from .models import User, VerifyCode

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'nickname', 'phone', 'email', 'is_active', 'data')


@admin.register(VerifyCode)
class VerifyCode(admin.ModelAdmin):
    list_display = ('code', 'email', 'send_type', 'send_time')