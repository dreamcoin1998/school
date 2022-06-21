from django.db import models
from yonghu.models import QQUser, WXUser, APPUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Message(models.Model):
    '''
    留言
    '''
    msg = models.CharField(max_length=128, verbose_name='留言')
    user = models.CharField(max_length=255, verbose_name="点赞用户ID", null=True)
    platform = models.CharField(max_length=10, verbose_name="平台", null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    floor = models.PositiveIntegerField(default=1, verbose_name='第几楼', editable=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        abstract = True


class MainMessage(Message):
    class Meta:
        ordering = ['create_time']
        verbose_name = '留言'
        verbose_name_plural = verbose_name


class ReplyMessage(Message):
    '''
    留言回复类
    '''
    reply_user = models.CharField(max_length=255, verbose_name="点赞用户ID", null=True)
    reply_platform = models.CharField(max_length=10, verbose_name="平台", null=True)

    def addReplyYonghuNickName(self):
        '''
        是回复,在回复内容前面加上相应内容;
        :return:
        '''
        self.msg = '回复' + self.reply_yonghu.nickName + ': ' + self.msg

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.addReplyYonghuNickName()
        super().save()

    class Meta:
        ordering = ['create_time']
        verbose_name = '留言回复'
        verbose_name_plural = verbose_name
