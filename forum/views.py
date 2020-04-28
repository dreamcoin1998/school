from utils.permissions.permissions import IsAuthenticated, IsOwnerOrReadOnlyInfo
from django.contrib.contenttypes.models import ContentType
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from .models import Post,PostType
from yonghu.models import Yonghu
from django.db.models.fields import exceptions
from .serializers import PostTypeSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from yonghu.views import CsrfExemptSessionAuthentication
from .serializers import PostSerializer
from utils.returnCode.ReturnCode import ReturnCode
from images.models import ImagePath
from utils.getPerson import GetPersonal
from images.getImagePath import GetImagePath
from readAndReplyNumAndLikes.views import ReadNumAnd
from Messages.getMessage import GetMessage
from django.db.models import Q
from readAndReplyNumAndLikes.getReadAndReplyNumLikes import GetReadAndReplyAndLikesNum
# Create your views here.

class ListCreatePost(mixins.CreateModelMixin,
                                    mixins.ListModelMixin,
                                    mixins.RetrieveModelMixin,
                                    viewsets.GenericViewSet,
                                    GetPersonal,
                                    GetImagePath,
                                    ReadNumAnd,
                                    GetMessage,
                                    GetReadAndReplyAndLikesNum):
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
            type_id = data.get('type_id')
            type_obj = PostType.objects.get(pk=int(type_id))
            yonghu_obj = self.get_person(request)
        except KeyError:
            return Response(ReturnCode(1, msg='object do not exists.'))
        try:
            post = Post()
            post.title = data.get('title')
            post.content = data.get('content')
            post.create_time = data.get('create_time')
            post.type = type_obj
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

    def index(self):
        '''
        默认列表
        :return:
        '''
        post = Post()
        return post.objects.all

    def post_detail_and_message_detail(self):
        '''
        获取帖子信息和帖子评论信息
        :return:
        '''
        if self.kwargs.get('pk'):
            pk = self.kwargs.get('pk')
            return Post.objects.filter(pk=pk, is_delete=False)
        else:
            return Post.objects.filter(is_delete=False)
        post_obj = post.objects.filter(pk=pk)
        message_obj = post_obj.message.all()
        return message_obj

    def post_list(self, request, *args, **kwargs):
        '''
        获取指定用户发表帖子
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        try:
            pk = request.session['pk']
        except KeyError:
            return Response(ReturnCode(1, msg='must login'),status=400)
        yonghu_obj = Yonghu.objects.get(pk=pk)
        post_obj = yonghu_obj.post.all()
        serializer = PostSerializer(post_obj,many=True)
        return Response(ReturnCode(0, data=serializer.data))

    def post_reply_and_like(self, request, *args, **kwargs):
        '''
        用户得到回复和点赞信息
        :return:
        '''
        post = Post()
        try:
            pk = request.session['pk']
        except KeyError:
            return Response(ReturnCode(1, msg='must login'), status=400)
        post_obj = post.objects.filter(pk=pk)
        message_obj = post_obj.message.all()
        return message_obj.reply_message





    def post_message_list(self):
        '''
        获取用户评论列表
        :return:
        '''
        yonghu_obj = self.get_person(self.request)
        message_obj = yonghu_obj.message.all()
        return message_obj


    def delete(self, request, *args, **kwargs):
        '''
        删除帖子和评论
        '''
        data = request.data.copy()
        post = Post()
        try:
            pk = request.session['pk']
        except KeyError:
            return Response(ReturnCode(1, msg='must login'),status=400)
        yonghu_obj = Yonghu.objects.get(pk=pk)
        return yonghu_obj.post.delete(object_id=post.pk)
        return yonghu_obj.message.delete(object_id=message.pk)



class ListPostByType(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    '''
    按分类搜索
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
def searchPostByNameOrContent(request):
        '''
        通过名字和关键字查询
        :param request:
        :return:
        '''
        query_set = request.query_params.get('q')
        post_obj = Post.objects.filter(Q(name__icontains=query_set) | Q(content__icontains=query_set))
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





