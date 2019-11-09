from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
import uuid
import random
from django.db.utils import IntegrityError


class VerifyCode(models.Model):
    """邮箱验证码"""
    code = models.CharField(verbose_name='验证码',max_length=10)
    # mobile = models.CharField(blank=True,null=True,verbose_name='电话',max_length=11)
    # add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')
    email = models.EmailField(verbose_name='邮箱',default='')
    send_choices = (
        ('register', '注册'),
        ('forget', '找回密码'),
        ('update_email', '修改邮箱'),
        ('email_login', '邮箱登录')
    )
    send_type = models.CharField(verbose_name='验证码类型', max_length=30, choices=send_choices, default='register')

    send_time = models.DateTimeField(auto_now=True, verbose_name='发送时间')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name='邮箱验证码'
        verbose_name_plural=verbose_name


class User(AbstractUser):
    """
    用户类
    """
    username = models.CharField(max_length=12, verbose_name='账号', unique=True)
    nickname = models.CharField(max_length=32, verbose_name='昵称', unique=True)
    phone = models.CharField(max_length=11, verbose_name='手机号码', default='')
    email = models.EmailField(unique=True,default='', verbose_name='邮箱')
    info = models.CharField(max_length=100, verbose_name='个人介绍', default='', null=True, blank=True)
    data = models.DateField(auto_now=True, verbose_name='创建时间')
    is_active = models.BooleanField(default=False, verbose_name='是否激活')

    def __str__(self):
        return self.nickname

    # 修改昵称和个人介绍
    def change_info(self, nickname, info):
        try:
            self.nickname = nickname
            self.info = info
            self.save()
            return True
        except IntegrityError as e:
            return False

    class Meta(AbstractUser.Meta):
        # swappable = 'AUTH_USER_MODEL'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    '''
    用户消息表
    '''
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user',verbose_name='收消息用户')
    to_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='to_user',verbose_name='发消息用户',blank=True,null=True)
    message = models.TextField(verbose_name='消息内容')
    ids = models.UUIDField(blank=True,null=True,verbose_name='评论有声书id',)
    url = models.CharField(max_length=200,verbose_name='地址',blank=True,null=True)
    is_supper = models.BooleanField(default=False,verbose_name='是系统消息')
    has_read = models.BooleanField(default=False, verbose_name='是否已读')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.message

    class Meta:
        verbose_name ='用户消息'
        verbose_name_plural=verbose_name
        ordering = ('-add_time',)