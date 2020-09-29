from django.db import models
from yonghu.models import Yonghu
from utils.uscSystem.getReadAndReplyNumLikes import GetReadAndReplyAndLikesNum
from utils.getImagePath import GetImagePath


class PostType(models.Model):
    '''
    帖子分类
    '''
    type_name = models.CharField(max_length=15, verbose_name='类型')

    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name = '帖子类型'
        verbose_name_plural = verbose_name


class Post(models.Model, GetReadAndReplyAndLikesNum, GetImagePath):
    '''
    发表帖子
    '''
    title = models.CharField(max_length=30, verbose_name='帖子标题')
    type = models.ForeignKey(PostType, on_delete=models.DO_NOTHING)
    content = models.TextField(verbose_name='帖子内容')
    yonghu = models.ForeignKey(Yonghu, on_delete=models.DO_NOTHING, verbose_name='发帖人')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_deleted = models.BooleanField(default=False, verbose_name='是否删除')

    @property
    def getType(self):
        return self.type.type_name

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_time']
        verbose_name = '发表帖子'
        verbose_name_plural = verbose_name

