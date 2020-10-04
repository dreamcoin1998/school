from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from yonghu.models import QQUser, WXUser, APPUser


class ReadAndReplyNum(models.Model):
    '''
    阅读数和回复数
    '''
    read_num = models.PositiveIntegerField(default=0, editable=False, verbose_name='阅读数')
    reply_num = models.PositiveIntegerField(default=0, editable=False, verbose_name='回复数')
    main_floor_num = models.PositiveIntegerField(default=0, editable=False, verbose_name='主楼数')
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = '阅读和回复数'
        verbose_name_plural = verbose_name


class Likes(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    like_num = models.IntegerField(default=0, verbose_name='点赞数')

    class Meta():
        verbose_name = '点赞数'
        verbose_name_plural = verbose_name


class LikeDetail(models.Model):
    likes = models.ForeignKey(Likes, on_delete=models.DO_NOTHING)
    user = models.CharField(max_length=255, verbose_name="点赞用户ID", null=True)
    platform = models.CharField(max_length=10, verbose_name="平台", null=True)
    is_liked = models.BooleanField(default=False, verbose_name='是否点赞')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')

    class Meta():
        verbose_name = '点赞细节'
        verbose_name_plural = verbose_name