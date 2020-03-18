from django.db import models
from yonghu.models import Yonghu
from readAndReplyNum.models import ReadAndReplyNum, ImagePath
from Messages .models import Message
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions


class Type(models.Model):
    type_name = models.CharField(max_length=20, verbose_name='类型')

    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name = '商品类型'
        verbose_name_plural = verbose_name


class GetReadAndReplyNum():
    @property
    def read_num(self):
        try:
            ct =ContentType.objects.get_for_model(self)
            readAndReplyNum = ReadAndReplyNum.objects.get(content_type=ct, object_id=self.pk)
            return readAndReplyNum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0

    @property
    def reply_num(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            readAndReplyNum = ReadAndReplyNum.objects.get(content_type=ct, object_id=self.pk)
            return readAndReplyNum.reply_num
        except exceptions.ObjectDoesNotExist:
            return 0


class GetImagePath():
    @property
    def imagePath(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            imgPath_objs = ImagePath.objects.filter(content_type=ct, object_id=self.pk)
            res = []
            for imgPath_obj in imgPath_objs:
                res.append(imgPath_obj.imgPath)
            return res
        except exceptions.ObjectDoesNotExist:
            return []


class GetMessage():
    @property
    def message(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            message_objs = Message.objects.filter(content_type=ct, object_id=self.pk)
            res = []
            for message_obj in message_objs:
                res.append(message_obj)
            return res
        except exceptions.ObjectDoesNotExist:
            return []


class Commody(models.Model, GetReadAndReplyNum, GetImagePath):
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
    yonghu = models.ForeignKey(Yonghu, on_delete=models.DO_NOTHING, related_name='commody')
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