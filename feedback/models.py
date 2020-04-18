from django.db import models
from transaction.models import GetImagePath
from yonghu.models import Yonghu


class Feedback(models.Model, GetImagePath):
    title = models.CharField(max_length=25, verbose_name='标题')
    content = models.TextField(verbose_name='反馈内容')
    status_code = (
        (0, '待处理'),
        (1, '已完成')
    )
    status = models.PositiveIntegerField(choices=status_code, verbose_name='状态')
    yonghu = models.ForeignKey(Yonghu, on_delete=models.DO_NOTHING, related_name='feedbacks')

    class Meta:
        verbose_name = '用户反馈'
        verbose_name_plural = verbose_name