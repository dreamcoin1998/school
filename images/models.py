from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


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
