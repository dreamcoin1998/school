from django.contrib import admin
from .models import MainMessage, ReplyMessage


@admin.register(MainMessage)
class MainMessageAdmin(admin.ModelAdmin):
    list_display = ('msg', 'create_time', 'floor', 'is_delete')


@admin.register(ReplyMessage)
class ReplyMessageAdmin(admin.ModelAdmin):
    list_display = ('msg', 'create_time', 'floor', 'is_delete')