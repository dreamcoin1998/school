from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from utils.ReturnCode import ReturnCode
from .models import MainMessage, ReplyMessage
from transaction.models import Commody
from readAndReplyNum.views import ReplyNumAdd
from .serializers import ReplyMessageSerializer, MainMessageSerializer
from utils.permissions import IsOwnerOrReadOnlyInfo
from yonghu.views import JSONWebTokenAuthentication, CsrfExemptSessionAuthentication
from django.contrib.contenttypes.models import ContentType
from utils.getPerson import GetPersonal
from yonghu.models import Yonghu
from django.db.models.fields import exceptions


class ListCreateCommodyMainMessage(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        viewsets.GenericViewSet,
                        ReplyNumAdd):
    '''
    返回或创建主楼评论
    '''
    serializer_class = MainMessageSerializer
    permission_classes = [IsOwnerOrReadOnlyInfo]
    authentication_classes = [JSONWebTokenAuthentication, CsrfExemptSessionAuthentication]

    def get_queryset(self):
        obj_id = self.request.query_params.get('id')
        if obj_id:
            commody_obj = Commody.objects.get(pk=int(obj_id))
            ct = ContentType.objects.get_for_model(commody_obj)
            return MainMessage.objects.filter(content_type=ct, object_id=commody_obj.pk, is_delete=False)
        return []

    def create(self, request, *args, **kwargs):
        obj_id = self.request.query_params.get('id')
        commody_obj = Commody.objects.get(pk=int(obj_id))
        return self.create_main_message_and_add_main_reply_num(commody_obj)


class ListCreateCommodyReplyMessage(mixins.ListModelMixin,
                                   mixins.CreateModelMixin,
                                    viewsets.GenericViewSet,
                                    ReplyNumAdd):
    '''
    返回或创建楼中楼评论
    '''
    serializer_class = ReplyMessageSerializer
    permission_classes = [IsOwnerOrReadOnlyInfo]
    authentication_classes = [JSONWebTokenAuthentication, CsrfExemptSessionAuthentication]

    def get_queryset(self):
        obj_id = self.request.query_params.get('id')
        floor = self.request.query_params.get('floor')
        if obj_id:
            commody_obj = Commody.objects.get(pk=int(obj_id))
            ct = ContentType.objects.get_for_model(commody_obj)
            if floor is None:
                return ReplyMessage.objects.filter(content_type=ct, object_id=commody_obj.pk, is_delete=False)
            else:
                return ReplyMessage.objects.filter(content_type=ct, object_id=commody_obj.pk, floor=int(floor), is_delete=False)
        else:
            return []

    def create(self, request, *args, **kwargs):
        obj_id = self.request.query_params.get('id')
        commody_obj = Commody.objects.get(pk=int(obj_id))
        return self.create_reply_message_and_add_reply_num(commody_obj)