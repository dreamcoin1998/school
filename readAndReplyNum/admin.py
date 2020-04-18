from django.contrib import admin
from .models import ReadAndReplyNum


@admin.register(ReadAndReplyNum)
class ReadAndReplyNumAdmin(admin.ModelAdmin):
    list_display = ('read_num', 'reply_num')