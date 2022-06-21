from rest_framework import mixins, viewsets
from rest_framework.response import Response
from utils.returnCode import ReturnCode
from .models import MainMessage, ReplyMessage
from transaction.models import Commody
from forum.models import Post
from readAndReplyNumAndLikes.views import ReplyNumAdd
from .serializers import ReplyMessageSerializer, MainMessageSerializer, MessageSerializer
from utils.permissions.permissions import IsOwnerOrReadOnlyInfo, IsAuthenticated
from yonghu.views import JSONWebTokenAuthentication, CsrfExemptSessionAuthentication
from django.contrib.contenttypes.models import ContentType
from utils.getPerson import GetPersonal
from django.db.models.fields import exceptions
from school import config


class GetObjectType:

    def get_object_instance(self):
        """
        获取评论信息对应的类的实例，是帖子还是商品
        :return:
        """
        obj_type = self.request.query_params.get('type')
        obj_id = self.request.query_params.get('id')
        if not obj_id:
            return None
        obj_type = obj_type.lower()
        try:
            # 从配置文件里面获取具体的类
            obj_type = eval(config.OBJ_TYPE[obj_type])
            obj = obj_type.objects.get(pk=int(obj_id))
        except KeyError:
            return None
        except exceptions.ObjectDoesNotExist:
            return None
        return obj


class ListCreateMainMessage(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            viewsets.GenericViewSet,
                            ReplyNumAdd,
                            GetObjectType):
    """
    返回或创建主楼评论
    """
    serializer_class = MainMessageSerializer
    permission_classes = [IsOwnerOrReadOnlyInfo]
    authentication_classes = [JSONWebTokenAuthentication, CsrfExemptSessionAuthentication]

    def get_queryset(self):
        obj = self.get_object_instance()
        if obj is None:
            return []
        ct = ContentType.objects.get_for_model(obj)
        return MainMessage.objects.filter(content_type=ct, object_id=obj.pk, is_delete=False)

    def create(self, request, *args, **kwargs):
        obj = self.get_object_instance()
        if obj is None:
            return Response(ReturnCode(1, msg='object do not exists.'), status=400)
        return self.create_main_message_and_add_main_reply_num(obj)


class ListCreateReplyMessage(mixins.ListModelMixin,
                             mixins.CreateModelMixin,
                             viewsets.GenericViewSet,
                             ReplyNumAdd,
                             GetObjectType):
    '''
    返回或创建楼中楼评论
    '''
    serializer_class = ReplyMessageSerializer
    permission_classes = [IsOwnerOrReadOnlyInfo]
    authentication_classes = [JSONWebTokenAuthentication, CsrfExemptSessionAuthentication]

    def get_queryset(self):
        floor = self.request.query_params.get('floor')
        obj = self.get_object_instance()
        if obj is None:
            return []
        ct = ContentType.objects.get_for_model(obj)
        if floor is None:
            return ReplyMessage.objects.filter(content_type=ct, object_id=obj.pk, is_delete=False)
        else:
            return ReplyMessage.objects.filter(content_type=ct, object_id=obj.pk, floor=int(floor), is_delete=False)

    def create(self, request, *args, **kwargs):
        obj = self.get_object_instance()
        if obj is None:
            return Response(ReturnCode(1, msg='object do not exists.'))
        return self.create_reply_message_and_add_reply_num(obj)


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
