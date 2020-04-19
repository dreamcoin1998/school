from django.db import models
from yonghu.models import Yonghu
from readAndReplyNum.getReadAndReplyNum import GetReadAndReplyNum
from images.getImagePath import GetImagePath


class Post(models.Model, GetReadAndReplyNum, GetImagePath):
    '''
    发表帖子
    '''
    title = models.CharField(max_length=30, verbose_name='帖子标题')
    content = models.TextField(verbose_name='帖子内容')
    yonghu = models.ForeignKey(Yonghu, on_delete=models.CASCADE, verbose_name='发帖人')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_deleted = models.BooleanField(default=False, verbose_name='是否删除')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_time']
        verbose_name = '发表帖子'
        verbose_name_plural = verbose_name
