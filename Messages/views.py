from rest_framework import mixins, viewsets
from rest_framework.response import Response
from utils.ReturnCode import ReturnCode
from .models import MainMessage, ReplyMessage
from transaction.models import Commody
from readAndReplyNumAndLikes.views import ReplyNumAdd
from .serializers import ReplyMessageSerializer, MainMessageSerializer, MessageSerializer
from utils.permissions import IsOwnerOrReadOnlyInfo, IsAuthenticated
from yonghu.views import JSONWebTokenAuthentication, CsrfExemptSessionAuthentication
from django.contrib.contenttypes.models import ContentType
from utils.getPerson import GetPersonal
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
            try:
            # 修复bug，这里用get如果找不到会报错 2020.04.05
                commody_obj = Commody.objects.get(pk=int(obj_id))
            except exceptions.ObjectDoesNotExist:
                return []
            ct = ContentType.objects.get_for_model(commody_obj)
            return MainMessage.objects.filter(content_type=ct, object_id=commody_obj.pk, is_delete=False)
        return []

    def create(self, request, *args, **kwargs):
        obj_id = self.request.query_params.get('id')
        try:
            commody_obj = Commody.objects.get(pk=int(obj_id))
        except exceptions.ObjectDoesNotExist:
            return Response(ReturnCode(1, msg='transaction object do not exists.'), status=400)
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
            try:
                commody_obj = Commody.objects.get(pk=int(obj_id))
            except exceptions.ObjectDoesNotExist:
                return []
            ct = ContentType.objects.get_for_model(commody_obj)
            if floor is None:
                return ReplyMessage.objects.filter(content_type=ct, object_id=commody_obj.pk, is_delete=False)
            else:
                return ReplyMessage.objects.filter(content_type=ct, object_id=commody_obj.pk, floor=int(floor), is_delete=False)
        else:
            return []

    def create(self, request, *args, **kwargs):
        obj_id = self.request.query_params.get('id')
        try:
            commody_obj = Commody.objects.get(pk=int(obj_id))
        except exceptions.ObjectDoesNotExist:
            return Response(ReturnCode(1, msg='commody object do not exists.'))
        return self.create_reply_message_and_add_reply_num(commody_obj)


class ListPersonalMessage(mixins.ListModelMixin,
                          viewsets.GenericViewSet,
                          GetPersonal):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnlyInfo]
    authentication_classes = [JSONWebTokenAuthentication, CsrfExemptSessionAuthentication]

    def get_queryset(self):
        yonghu_obj = self.get_person(self.request)
        message_obj = yonghu_obj.message.all()
        return message_obj