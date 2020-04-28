from django.contrib import admin
from .models import ReadAndReplyNum,Likes,LikeDetail


@admin.register(ReadAndReplyNum)
class ReadAndReplyNumAdmin(admin.ModelAdmin):
    list_display = ('read_num', 'reply_num')

@admin.register(Likes)
class LikesAdmin(admin.ModelAdmin):
    list_display = ('like_num', )

@admin.register(LikeDetail)
class LikeDetail(admin.ModelAdmin):
    list_display = ('is_liked','created_time')