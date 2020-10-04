from django.db.models.fields import exceptions
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from yonghu.models import QQUser
from rest_framework.response import Response
from utils.returnCode.ReturnCode import ReturnCode
from Messages.models import MainMessage, ReplyMessage
from .models import ReadAndReplyNum,LikeDetail,Likes


class ReadNumAnd:
    @transaction.atomic
    def add_read_num(self):
        '''
        添加阅读数

        如果存在session，返回True,
        如果不存在session,设置一个事务增加阅读数，乐观锁，循环三次查看read_num == read_num_new - 1，
        否则返回False
        '''
        '''
        修改自dreamcoin于 2020.04.16 (改变session的维护方式)
        '''
        # path_info = self.request.session.get(self.request.get_full_path())
        path_info = self.request.get_full_path()
        obj_session = self.request.session.get('has_read') if self.request.session.get('has_read') else ''
        # print(self.request.path_info)
        if path_info in obj_session:
            return True
        else:
            '''2020.04.21'''
            # self.request.session['has_read'] = obj_session
            # self.request.session[self.request.get_full_path()] = '1'
            self.request.session['has_read'] = obj_session
            self.request.session['has_read'] += self.request.get_full_path()
            obj = self.get_object()
            ct = ContentType.objects.get_for_model(obj)
            sid = transaction.savepoint()
            num = 0
            # 乐观锁，放置多个进程修改同一个数据
            while num < 3:
                read_num = obj.read_num
                try:
                    read_and_reply_num_obj = ReadAndReplyNum.objects.get(content_type=ct,
                                                                         object_id=obj.pk)
                except exceptions.ObjectDoesNotExist:
                    read_and_reply_num_obj = ReadAndReplyNum()
                    read_and_reply_num_obj.content_type = ct
                    read_and_reply_num_obj.object_id = obj.pk
                read_and_reply_num_obj.read_num += 1
                read_and_reply_num_obj.save()
                read_num_new = obj.read_num
                # 检查是否有其他的进程已经修改了这个字段
                if read_num == read_num_new - 1:
                    return True
                else:
                    num += 1
                    transaction.savepoint_rollback(sid)
            return False


class ReplyNumAdd:

    def _get_create_yonghu(self):
        '''
        获取提交留言的用户
        '''
        pk = self.request.session['pk']
        # pk = 'test'
        yonghu_obj = QQUser.objects.get(pk=pk)
        return yonghu_obj

    def _get_or_create_read_and_reply_num_model(self, ct, obj):
        '''
        获取或创建ReadAndReplyNum模型
        :param ct:
        :param obj:
        :return:
        '''
        try:
            read_and_reply_num_obj = ReadAndReplyNum.objects.get(content_type=ct,
                                                                 object_id=obj.pk)
            return read_and_reply_num_obj
        except exceptions.ObjectDoesNotExist:
            read_and_reply_num_obj = ReadAndReplyNum()
            read_and_reply_num_obj.content_type = ct
            read_and_reply_num_obj.object_id = obj.pk
            return read_and_reply_num_obj

    @transaction.atomic
    def create_reply_message_and_add_reply_num(self, obj):
        '''
        提交留言增加reply_num事务，乐观锁，循环三次
        '''
        ct = ContentType.objects.get_for_model(obj)
        try:
            yonghu_obj = self._get_create_yonghu()
        except KeyError:
            return Response(ReturnCode(1, msg='not login.'))
        except exceptions.ObjectDoesNotExist:
            return Response(ReturnCode(1, msg='user not find, cookie error.'))
        read_and_reply_num_obj = self._get_or_create_read_and_reply_num_model(ct, obj)
        msg = self.request.data.get('msg')
        reply_yonghu_pk = self.request.data.get('reply_yonghu_pk')
        reply_yonghu_obj = QQUser.objects.get(pk=reply_yonghu_pk)
        floor = int(self.request.query_params.get('floor'))
        sid = transaction.savepoint()
        num = 0
        while num < 3:
            reply_num = obj.reply_num
            reply_message = ReplyMessage()
            reply_message.msg = msg
            reply_message.yonghu = yonghu_obj
            reply_message.content_type = ct
            reply_message.object_id = obj.pk
            reply_message.floor = floor
            reply_message.reply_yonghu = reply_yonghu_obj
            reply_message.save()
            read_and_reply_num_obj.reply_num += 1
            read_and_reply_num_obj.save()
            new_reply_num = obj.reply_num
            if reply_num == new_reply_num - 1:
                return Response(ReturnCode(0))
            else:
                num += 1
                transaction.savepoint_rollback(sid)
            return Response(ReturnCode(1, msg='create message error.'))

    @transaction.atomic
    def create_main_message_and_add_main_reply_num(self, obj):
        '''
        创建主楼评论并且增加回复数
        '''
        ct = ContentType.objects.get_for_model(obj)
        try:
            yonghu_obj = self._get_create_yonghu()
        except KeyError:
            return Response(ReturnCode(1, msg='not login.'))
        except exceptions.ObjectDoesNotExist:
            return Response(ReturnCode(1, msg='user not find, cookie error.'))
        read_and_reply_num_obj = self._get_or_create_read_and_reply_num_model(ct, obj)
        msg = self.request.data.get('msg')
        sid = transaction.savepoint()
        num = 0
        while num < 3:
            reply_num = obj.reply_num
            main_floor_num = obj.main_floor_num
            main_message = MainMessage()
            main_message.msg = msg
            main_message.yonghu = yonghu_obj
            main_message.content_type = ct
            main_message.object_id = obj.pk
            main_message.floor = main_floor_num + 1
            main_message.save()
            read_and_reply_num_obj.reply_num += 1
            read_and_reply_num_obj.main_floor_num += 1
            read_and_reply_num_obj.save()
            new_reply_num = obj.reply_num
            new_main_floor_num = obj.main_floor_num
            if reply_num == new_reply_num - 1 and main_floor_num == new_main_floor_num - 1:
                return Response(ReturnCode(0))
            else:
                num += 1
                transaction.savepoint_rollback(sid)
            return Response(ReturnCode(1, msg='create message error.'))

    @transaction.atomic
    class LikesAdd:
        def like_record(self,request):
            yonghu = request.yonghu
            content_type = request.GET.get('content_type')
            object_id = request.GET.get('object_id')
            is_liked = request.GET.get('is_liked')
            content_type = ContentType.objects.get(model=content_type)

            if is_liked == True:
                like_detail, created = LikeDetail.objects.get_or_create(content_type,object_id=object_id,yonghu=yonghu)
                #准备进行点赞
                if created:
                    #可以点赞
                    likes, created = Likes.objects.get_or_create(content_type,object_id=object_id)
                    obj = self.get_object()
                    ct = ContentType.objects.get_for_model(obj)
                    sid = transaction.savepoint()
                    num = 0
                    while num < 3:
                        like_num = obj.like_num
                        likes_obj = Likes()
                        likes_obj.content_type = ct
                        likes_obj.object_id = obj.pk
                        likes.like_num += 1
                        likes.save()
                        like_num_new = obj.like_num
                        if like_num == like_num_new - 1:
                            return True
                        else:
                            num += 1
                            transaction.savepoint_rollback(sid)
                        return False
                        return Response(ReturnCode(0))
                    else:
                        return Response(ReturnCode(1, msg='already liked it'))
                else:
                    #准备取消点赞
                    if LikeDetail.objects.filter(content_type, object_id=object_id,
                                                            yonghu=yonghu).exist():
                        like_detail = LikeDetail.objects.get(content_type, object_id=object_id,yonghu=yonghu)
                        like_detail.delete()
                        likes, created = Likes.objects.get_or_create(content_type,object_id=object_id)
                        likes.like_num -= 1
                        likes.save()
                        return Response(ReturnCode(0))
                    else:
                        return Response(ReturnCode(1, msg='does not exist'))
