from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class ReadAndReplyNum(models.Model):
    '''
    阅读数和回复数
    '''
    read_num = models.PositiveIntegerField(default=0, editable=False, verbose_name='阅读数')
    reply_num = models.PositiveIntegerField(default=0, editable=False, verbose_name='回复数')
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = '阅读和回复数'
        verbose_name_plural = verbose_name


class ImagePath(models.Model):
    '''
    图片链接
    '''
    imgPath = models.URLField(verbose_name='图片链接')
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = '图片'
        verbose_name_plural = verbose_name