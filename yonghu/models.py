# -*- coding: utf-8 -*-
from django.db import models


class UserCommon(models.Model):
    nickName = models.CharField(max_length=64, verbose_name='昵称', null=True)
    GENDER = (
        (0, '未知'),
        (1, '男性'),
        (2, '女性')
    )
    gender = models.IntegerField(choices=GENDER, verbose_name='性别', default=0)
    country = models.CharField(max_length=16, verbose_name='国家', default='')
    province = models.CharField(max_length=32, verbose_name='省份', default='')
    city = models.CharField(max_length=16, verbose_name='城市', default='')
    avatarUrl = models.URLField(default='', null=True, blank=True, verbose_name='头像地址')
    is_auth = models.BooleanField(default=False, verbose_name='是否认证')
    is_auth_new = models.BooleanField(default=False, verbose_name='是否认证(新系统)')

    class Meta:
        abstract = True
        verbose_name = "通用用户"
        verbose_name_plural = verbose_name


class QQUser(UserCommon):
    openid = models.CharField(max_length=64, unique=True, primary_key=True)

    class Meta:
        verbose_name = 'QQ用户'
        verbose_name_plural = verbose_name


class WXUser(UserCommon):
    openid = models.CharField(max_length=64, unique=True, primary_key=True)

    class Meta:
        verbose_name = '微信用户'
        verbose_name_plural = verbose_name


class APPUser(UserCommon):
    email = models.EmailField(verbose_name="邮箱地址", unique=True)
    phone = models.CharField(max_length=11, verbose_name="电话号码", unique=True, null=True)
    password = models.CharField(max_length=50, verbose_name="密码")

    class Meta:
        verbose_name = 'APP用户'
        verbose_name_plural = verbose_name
        indexes = [models.Index(fields=['email'])]


class UscInfo(models.Model):
    UserName = models.CharField(max_length=16, verbose_name='校园网用户名', unique=True, null=True)
    Password = models.CharField(max_length=32, verbose_name='校园网密码', null=True)
    QQUser = models.CharField(max_length=255, verbose_name='QQ用户ID', null=True, db_index=True)
    WXUser = models.CharField(max_length=255, verbose_name='微信用户ID', null=True, db_index=True)
    APPUser = models.CharField(max_length=255, verbose_name='APP用户ID', null=True, db_index=True)

    class Meta:
        verbose_name = '南华大学教务在线用户信息'
        verbose_name_plural = verbose_name


class NewUSCINFO(models.Model):
    UserName = models.CharField(max_length=16, verbose_name='校园网用户名', unique=True, null=True)
    Password = models.CharField(max_length=32, verbose_name='校园网密码', null=True)
    QQUser = models.CharField(max_length=255, verbose_name='QQ用户ID', null=True, db_index=True)
    WXUser = models.CharField(max_length=255, verbose_name='微信用户ID', null=True, db_index=True)
    APPUser = models.CharField(max_length=255, verbose_name='APP用户ID', null=True, db_index=True)

    class Meta:
        verbose_name = '南华大学新版教务在线用户信息'
        verbose_name_plural = verbose_name
