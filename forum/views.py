from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from utils.permissions import IsOwnerOrReadOnlyInfo
from utils.permissions import IsAuthenticated, IsOwnerOrReadOnlyInfo, CreateOrReadOnlyInfo
from utils import code2Session
from django.contrib.contenttypes.models import ContentType
from rest_framework import mixins, viewsets
from Messages.serializers import MainMessageSerializer,MessageSerializer,ReplyMessageSerializer
from rest_framework.response import Response
from utils.ReturnCode import ReturnCode
from .models import Post
from yonghu.models import Yonghu
from django.db.models.fields import exceptions
from .serializers import PostSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth.backends import ModelBackend
from yonghu.views import CsrfExemptSessionAuthentication
from .serializers import PostSerializer
from utils.ReturnCode import ReturnCode
from images.models import ImagePath
from utils.getPerson import GetPersonal
from images.views import GetImagePath
from readAndReplyNum.views import ReadNumAnd, ReplyNumAdd
# Create your views here.

class ListCreatePost(mixins.CreateModelMixin,
                                    mixins.ListModelMixin,
                                    mixins.RetrieveModelMixin,
                                    viewsets.GenericViewSet,
                                    GetPersonal,
                                    GetImagePath,
                                    ReadNumAnd):
    lookup_field = 'pk'
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnlyInfo]
    authentication_classes = [JSONWebTokenAuthentication, CsrfExemptSessionAuthentication]

    def get_queryset(self):
        if self.kwargs.get('pk'):
            pk = self.kwargs.get('pk')
            return Post.objects.filter(pk=pk,is_delete=False)
        else:
            return Post.objects.filter(is_delete=False)

    def retrieve(self, request, *args, **kwargs):
        if self.add_read_num():
            return super().retrieve(self, request, *args, **kwargs)
        else:
            return Response(ReturnCode(1, msg='request error.'), status=404)

    def create(self, request, *args, **kwargs):
        '''
        发表帖子
        '''
        data = request.data.copy()
        try:
            yonghu_obj = self.get_person(request)
        except KeyError:
            return Response(ReturnCode(1, msg='object do not exists.'))
        try:
            post = Post()
            post.title = data.get('title')
            post.content = data.get('content')
            post.create_time = data.get('create_time')
            post.yonghu = yonghu_obj
            post.save()
            ct = ContentType.objects.get_for_model(post)
            imagePaths = self.get_image_path(request)
            for imagePath in imagePaths:
                img_path_obj = ImagePath()
                img_path_obj.content_type = ct
                img_path_obj.object_id = post.pk
                img_path_obj.imgPath = imagePath
                img_path_obj.save()
            serializer = PostSerializer(post)
            return Response(ReturnCode(0, data=serializer.data))
        except exceptions.FieldError:
            return Response(ReturnCode(1, msg='field error.'))

class ListCreatePostMainMessage(mixins.ListModelMixin,
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
                post_obj = post.objects.get(pk=int(obj_id))
            except exceptions.ObjectDoesNotExist:
                return []
            ct = ContentType.objects.get_for_model(post_obj)
            return MainMessage.objects.filter(content_type=ct, object_id=post_obj.pk, is_delete=False)
        return []

    def create(self, request, *args, **kwargs):
        obj_id = self.request.query_params.get('id')
        try:
            post_obj = post.objects.get(pk=int(obj_id))
        except exceptions.ObjectDoesNotExist:
            return Response(ReturnCode(1, msg='post object does not exists.'), status=400)
        return self.create_main_message_and_add_main_reply_num(post_obj)

class ListCreatePostReplyMessage(mixins.ListModelMixin,
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
                post_obj = Post.objects.get(pk=int(obj_id))
            except exceptions.ObjectDoesNotExist:
                return []
            ct = ContentType.objects.get_for_model(post_obj)
            if floor is None:
                return ReplyMessage.objects.filter(content_type=ct, object_id=post_obj.pk, is_delete=False)
            else:
                return ReplyMessage.objects.filter(content_type=ct, object_id=post_obj.pk, floor=int(floor),
                                                       is_delete=False)
        else:
            return []

    def create(self, request, *args, **kwargs):
        obj_id = self.request.query_params.get('id')
        try:
            post_obj = Post.objects.get(pk=int(obj_id))
        except exceptions.ObjectDoesNotExist:
            return Response(ReturnCode(1, msg='post object does not exists.'))
        return self.create_reply_message_and_add_reply_num(post_obj)

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

