from django.db import models
from yonghu.models import Yonghu

# Create your models here.
class Commody(models.Model):
    '''
    商品信息类
    '''
    name = models.CharField(max_length=64, verbose_name='商品名称')
    description = models.TextField(verbose_name='描述信息')
    price = models.FloatField(verbose_name='价格')
    read_num = models.IntegerField(verbose_name='浏览次数', default=0)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    type = models.CharField(max_length=12, verbose_name='类型')
    qq = models.CharField(max_length=15, verbose_name='QQ号', default='')
    wx = models.CharField(max_length=25, verbose_name='微信号', default='')
    phone_number = models.CharField(max_length=11, verbose_name='电话号码', default='')
    yonghu = models.ForeignKey(Yonghu, on_delete=models.DO_NOTHING, related_name='commody')
    replyNum = models.IntegerField(verbose_name='留言数')
    floorNum = models.IntegerField(verbose_name='主楼数')

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name


class ImagePath(models.Model):
    '''
    商品图片链接
    '''
    imgPath = models.URLField(verbose_name='图片链接')
    commody = models.ForeignKey(Commody, on_delete=models.DO_NOTHING, related_name='imagePath')

    class Meta:
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name


class Message(models.Model):
    '''
    留言
    '''
    msg = models.CharField(max_length=128, verbose_name='留言')
    commody = models.ForeignKey(Commody, on_delete=models.DO_NOTHING, related_name='message')
    yonghu = models.ForeignKey(Yonghu, on_delete=models.DO_NOTHING, related_name='message')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    is_reply = models.BooleanField(default=False, verbose_name='是否是楼中楼')
    reply_yonghu = models.OneToOneField(Yonghu, on_delete=models.DO_NOTHING, related_name='reply_message')
    floor = models.CharField(max_length=10, default='', verbose_name='第几楼')

    def addReplyYonghuNickName(self):
        '''
        如果是回复的话，在回复内容前面加上相应内容;
        :return:
        '''
        if self.is_reply:
            self.msg = self.reply_yonghu.nickName + ': ' + self.msg

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.addReplyYonghuNickName()
        super().save()

    class Meta:
        verbose_name = '留言'
        verbose_name_plural = verbose_name