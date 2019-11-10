# from __future__ import absolute_import
#
# import datetime
# from configparser import ConfigParser
# from time import sleep
#
# import requests
# from celery import shared_task
#
#
# from django.core.mail import send_mail
#
# from random import Random
# import random
#
# # from .models import VerifyCode
# from school import settings
# from school.celery import app
#
#
# def delete_code_record(email, send_type):
#     '''
#     发送验证码之前先删除之前发送的验证码记录
#     :param email:
#     :param send_type:
#     :return:
#     '''
#     yzms = VerifyCode.objects.filter(email=email, send_type=send_type)  # 验证码集合
#     for yzm in yzms:
#         # print(yzm)
#         yzm.delete()
#
#
# def random_str(randomlength=8):
#     '''
#     随机验证码
#     :param randomlength:
#     :return:
#     '''
#     str=""
#     chars="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
#     lenght = len(chars)-1
#     for i in range(randomlength):
#         str+=chars[random.randint(0,lenght)]
#     print(str)
#     return str
#
#
# @app.task()
# def send_register_email(email,username=None,token=None,send_type='register'):
#     """
#     登录注册等邮件发送
#     用户注册时，只需要访问链接就可以
#     密码重置和修改邮箱都需要验证验证码
#     :param email:
#     :param username:
#     :param token:
#     :param send_type:
#     :return:
#     """
#     code = random_str(4)
#     email_title = ''
#     email_body = ''
#     if send_type =='register':
#         email_title = '注册用户验证信息'
#         email_body = "\n".join(['{0},欢迎'.format(username), '注册，请访问该链接，完成用户验证,该链接1个小时内有效',
#                                  '/'.join([settings.DOMAIN, 'activate?token=' + token])])
#         print('========发送邮件中')
#         send_stutas = send_mail(email_title, email_body, settings.EMAIL_HOST_USER, [email])
#         print(send_stutas)
#         if send_stutas:
#             print('========发送成功')
#             pass
#     elif send_type == 'email_login':
#         '''先删除当前邮箱之前发的所有验证码'''
#         delete_code_record(email, send_type)
#         VerifyCode.objects.create(code=code, email=email, send_type=send_type)
#         email_title = '邮箱登录验证码'
#         email_body = "你的邮箱登录验证码为:{0}。如非本人操作请忽略,此验证码5分钟后失效。".format(code)
#         print('========发送邮件中')
#         send_stutas = send_mail(email_title, email_body, settings.EMAIL_HOST_USER, [email])
#         if send_stutas:
#             print('=========发送成功')
#             pass
#     elif send_type == 'forget':
#         delete_code_record(email, send_type)
#         VerifyCode.objects.create(code=code, email=email, send_type=send_type)
#         email_title = '密码重置'
#         email_body = "你的密码重置验证码为:{0}。如非本人操作请忽略,此验证码5分钟后失效。".format(code)
#         print('========发送邮件中')
#         send_stutas = send_mail(email_title, email_body, settings.EMAIL_HOST_USER, [email])
#         if send_stutas:
#             print('========发送成功')
#             pass
#     elif send_type =='update_email':
#         delete_code_record(email, send_type)
#         VerifyCode.objects.create(code=code, email=email, send_type=send_type)
#         email_title = '修改邮箱'
#         email_body = "你的修改邮箱验证码为:{0}。如非本人操作请忽略,此验证码5分钟后失效。".format(code)
#         print('========发送邮件中')
#         send_stutas = send_mail(email_title, email_body, settings.EMAIL_HOST_USER, [email])
#         if send_stutas:
#             print('========发送成功')
#             pass
