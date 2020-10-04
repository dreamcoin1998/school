from django.db import models
from yonghu.models import QQUser, WXUser, APPUser
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
    user = models.CharField(max_length=255, verbose_name="点赞用户ID", null=True)
    platform = models.CharField(max_length=10, verbose_name="平台", null=True)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_deleted = models.BooleanField(default=False, verbose_name='是否删除')

    @property
    def getType(self):
        return self.type.type_name

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        yonghu_objs = QQUser.objects.filter(openid=self.yonghu)
        if yonghu_objs:
            super(Post, self).save()
        else:
            raise ValueError("the user objects (openid: %s) dont exists." % self.yonghu)

    class Meta:
        ordering = ['-created_time']
        verbose_name = '发表帖子'
        verbose_name_plural = verbose_name
