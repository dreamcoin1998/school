from django.db import models
from yonghu.models import Yonghu
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Message(models.Model):
    '''
    留言
    '''
    msg = models.CharField(max_length=128, verbose_name='留言')
    yonghu = models.ForeignKey(Yonghu, on_delete=models.DO_NOTHING, related_name='message')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    # is_reply = models.BooleanField(default=False, verbose_name='是否是楼中楼')
    floor = models.PositiveIntegerField(default=1, verbose_name='第几楼', editable=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    # class Meta:
    #     abstract = True


class MainMessage(Message):
    # yonghu = models.ForeignKey(Yonghu, on_delete=models.DO_NOTHING, related_name='main_message')
    class Meta:
        ordering = ['create_time']
        verbose_name = '留言'
        verbose_name_plural = verbose_name


class ReplyMessage(Message):
    '''
    留言回复类
    '''
    reply_yonghu = models.ForeignKey(Yonghu, on_delete=models.DO_NOTHING, related_name='reply_message')
    # comment = models.ForeignKey(MainMessage, related_name='reply_message', on_delete=models.DO_NOTHING)

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