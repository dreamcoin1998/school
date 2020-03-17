from django.contrib import admin
from .models import Commody, Message, ImagePath

# Register your models here.
@admin.register(Commody)
class CommodyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'read_num', 'create_time', 'type', 'qq', 'wx', 'phone_number', 'replyNum', 'floorNum')


@admin.register(ImagePath)
class ImagePathAdmin(admin.ModelAdmin):
    list_display = ('imgPath',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('msg', 'create_time', 'is_reply', 'floor')