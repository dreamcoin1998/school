from django.db import models
from yonghu.models import QQUser, WXUser, APPUser
from django.db.models.fields import exceptions
from utils.getImagePath import GetImagePath
from utils.uscSystem.getReadAndReplyNumLikes import GetReadAndReplyAndLikesNum


class Type(models.Model):
    type_name = models.CharField(max_length=20, verbose_name='类型')

    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name = '商品类型'
        verbose_name_plural = verbose_name


class Commody(models.Model, GetReadAndReplyAndLikesNum, GetImagePath):
    '''
    商品信息类
    '''
    name = models.CharField(max_length=64, verbose_name='商品名称')
    description = models.TextField(verbose_name='描述信息')
    price = models.FloatField(verbose_name='价格')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    type = models.ForeignKey(Type, on_delete=models.DO_NOTHING, related_name='commody')
    qq = models.CharField(max_length=15, verbose_name='QQ号', default='', null=True, blank=True)
    wx = models.CharField(max_length=25, verbose_name='微信号', default='', null=True, blank=True)
    phone_number = models.CharField(max_length=11, verbose_name='电话号码', default='', null=True, blank=True)
    user = models.CharField(max_length=255, verbose_name="发表用户", null=True)
    platform = models.CharField(max_length=10, verbose_name="平台", null=True)
    is_end = models.BooleanField(default=False, verbose_name='是否结束')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    @property
    def getType(self):
        return self.type.type_name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # print(self.type.name)
        if self.qq or self.wx or self.phone_number:
            super(Commody, self).save()
        else:
            raise exceptions.FieldDoesNotExist

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name
