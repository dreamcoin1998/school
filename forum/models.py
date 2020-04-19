from django.db import models
from yonghu.models import Yonghu
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from Messages.models import MainMessage,Message,ReplyMessage

# Create your models here.
class Post(models.Model):
    '''
    发表帖子
    '''
    title = models.CharField(max_length=30,verbose_name='帖子标题')
    content = models.TextField(verbose_name='帖子内容')
    yonghu = models.ForeignKey(Yonghu, on_delete=models.CASCADE,verbose_name='发帖人')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    read_nums = models.IntegerField(default=False, verbose_name='阅读次数')
    is_deleted = models.BooleanField(default=False, verbose_name='是否删除')
    num_views = models.IntegerField(default=False, verbose_name='浏览量')
    @property
    def __str__(self):
        return self.title

class MainPost(Post):
    class Meta:
        ordering = ['-created_time']
        verbose_name = '发表帖子'
        verbose_name_plural = verbose_name

class PostMessage(Message,models.Model):
    pass