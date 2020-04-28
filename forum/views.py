from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from utils.permissions import IsOwnerOrReadOnlyInfo
from utils.permissions import IsAuthenticated, IsOwnerOrReadOnlyInfo, CreateOrReadOnlyInfo
from utils import code2Session
from django.contrib.contenttypes.models import ContentType
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from utils.ReturnCode import ReturnCode
from .models import Post,PostType
from yonghu.models import Yonghu
from django.db.models.fields import exceptions
from .serializers import PostSerializer,PostTypeSerializer
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
from images.getImagePath import GetImagePath
from readAndReplyNum.views import ReadNumAnd, ReplyNumAdd
from Messages.getMessage import GetMessage
from django.db.models import Q
# Create your views here.

class ListCreatePost(mixins.CreateModelMixin,
                                    mixins.ListModelMixin,
                                    mixins.RetrieveModelMixin,
                                    viewsets.GenericViewSet,
                                    GetPersonal,
                                    GetImagePath,
                                    ReadNumAnd,
                                    GetMessage):
    lookup_field = 'pk'
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnlyInfo]
    authentication_classes = [JSONWebTokenAuthentication, CsrfExemptSessionAuthentication]

    def get_queryset(self):
        if self.kwargs.get('pk'):
            pk = self.kwargs.get('pk')
            return Post.objects.filter(pk=pk,is_deleted=False)
        else:
            return Post.objects.filter(is_deleted=False)

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
            return Response(ReturnCode(1, msg='object does not exists.'))
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
            Messages = self.get_message(request)
            for Message in Messages:
                message_obj = Message()
                message_obj.content_type = ct
                message_obj.object_id = post.pk
                message_obj.Message = Message
                message_obj.save()
            serializer = PostSerializer(post)
            return Response(ReturnCode(0, data=serializer.data))
        except exceptions.FieldError:
            return Response(ReturnCode(1, msg='field error.'))

    def delete(self, request, *args, **kwargs):
        '''
        删除帖子
        '''
        post_obj = self.get_object()
        data = request.data.copy()
        if data.get('is_delete'):
            data.pop('is_delete')
        if data.get('create_time'):
            data.pop('create_time')
        serializer = PostSerializer(post_obj, data=data)
        if serializer.is_valid():
            return Response(ReturnCode(0, msg='success.', data=serializer.data))
        else:
            return Response(ReturnCode(1, msg='data invalid.'))


class ListPostByType(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    '''
    按分类
    '''
    lookup_field = 'pk'
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnlyInfo]
    authentication_classes = [JSONWebTokenAuthentication, CsrfExemptSessionAuthentication]

    def get_queryset(self):
        if self.request.query_params.get('id'):
            type = self.request.query_params.get('id')
            type_obj = PostType.objects.get(pk=int(type))
            return type_obj.post.filter(is_deleted=False)
        else:
            return Post.objects.filter(is_deleted=False)

@csrf_exempt
@api_view()
def searchPostByNameOrDescription(request):
        '''
        通过名字和关键字查询
        :param request:
        :return:
        '''
        query_set = request.query_params.get('q')
        post_obj = Post.objects.filter(Q(name__icontains=query_set) | Q(description__icontains=query_set))
        serializer = PostSerializer(post_obj, many=True)
        return Response(ReturnCode(0, data=serializer.data))

class PostListType(mixins.ListModelMixin,
                viewsets.GenericViewSet):
    '''
    帖子分类
    '''
    lookup_field = 'pk'
    serializer_class = PostTypeSerializer
    permission_classes = [IsOwnerOrReadOnlyInfo, IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, CsrfExemptSessionAuthentication]

    def get_queryset(self):
        return PostType.objects.filter(is_deleted=False)



