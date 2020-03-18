from django.contrib import admin
from .models import ImagePath, ReadAndReplyNum

# Register your models here.
@admin.register(ImagePath)
class ImagePathAdmin(admin.ModelAdmin):
    list_display = ('imgPath',)


@admin.register(ReadAndReplyNum)
class ReadAndReplyNumAdmin(admin.ModelAdmin):
    list_display = ('read_num', 'reply_num')