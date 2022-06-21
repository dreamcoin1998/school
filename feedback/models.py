from django.db import models
from transaction.models import GetImagePath
from yonghu.models import QQUser, WXUser, APPUser


class Feedback(models.Model, GetImagePath):
    title = models.CharField(max_length=25, verbose_name='标题')
    content = models.TextField(verbose_name='反馈内容')
    status_code = (
        (0, '待处理'),
        (1, '已完成')
    )
    status = models.PositiveIntegerField(choices=status_code, verbose_name='状态')
    user = models.CharField(max_length=255, verbose_name="点赞用户ID", null=True)
    platform = models.CharField(max_length=10, verbose_name="平台", null=True)

    class Meta:
        verbose_name = '用户反馈'
        verbose_name_plural = verbose_name
