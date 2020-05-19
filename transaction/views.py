from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from utils.permissions.permissions import IsAuthenticated, IsOwnerOrReadOnlyInfo
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from yonghu.views import CsrfExemptSessionAuthentication
from .models import Commody, Type
from .serializers import CommodySerializer, TypeSerializer
from utils.returnCode.ReturnCode import ReturnCode
from django.db.models.fields import exceptions
from django.db.models import Q
from images.models import ImagePath
from django.contrib.contenttypes.models import ContentType
from utils.getPerson import GetPersonal
from images.views import GetImagePath
from readAndReplyNumAndLikes.views import ReadNumAnd


class CreateListRetrieveTransaction(mixins.CreateModelMixin,
                                    mixins.ListModelMixin,
                                    mixins.RetrieveModelMixin,
                                    viewsets.GenericViewSet,
                                    GetPersonal,
                                    GetImagePath,
                                    ReadNumAnd):
    lookup_field = 'pk'
    serializer_class = CommodySerializer
    permission_classes = [IsOwnerOrReadOnlyInfo]
    authentication_classes = [JSONWebTokenAuthentication, CsrfExemptSessionAuthentication]

    def get_queryset(self):
        if self.kwargs.get('pk'):
            pk = self.kwargs.get('pk')
            return Commody.objects.filter(pk=pk, is_end=False, is_delete=False)
        else:
            return Commody.objects.filter(is_end=False, is_delete=False)

    def retrieve(self, request, *args, **kwargs):
        if self.add_read_num():
            return super().retrieve(self, request, *args, **kwargs)
        else:
            return Response(ReturnCode(1, msg='request error.'), status=404)

    def create(self, request, *args, **kwargs):
        '''
        创建商品信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        data = request.data.copy()
        try:
            type_id = data.get('type_id')
            type_obj = Type.objects.get(pk=int(type_id))
            yonghu_obj = self.get_person(request)
        except KeyError:
            return Response(ReturnCode(1, msg='object do not exists.'))
        try:
            commody = Commody()
            commody.name = data.get('name')
            commody.description = data.get('description')
            commody.price = data.get('price')
            commody.type = type_obj
            commody.qq = data.get('qq')
            commody.wx = data.get('wx')
            commody.phone_number = data.get('phone_number')
            commody.yonghu = yonghu_obj
            commody.save()
            ct = ContentType.objects.get_for_model(commody)
            imagePaths = self.get_image_path(request)
            for imagePath in imagePaths:
                img_path_obj = ImagePath()
                img_path_obj.content_type = ct
                img_path_obj.object_id = commody.pk
                img_path_obj.imgPath = imagePath
                img_path_obj.save()
            serializer = CommodySerializer(commody)
            return Response(ReturnCode(0, data=serializer.data))
        except exceptions.FieldDoesNotExist:
            return Response(ReturnCode(1, msg='qq wx and phone_number must have at least one.'))
        except exceptions.FieldError:
            return Response(ReturnCode(1, msg='field error.'))


class ListCommodyByType(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    lookup_field = 'pk'
    serializer_class = CommodySerializer
    permission_classes = [IsOwnerOrReadOnlyInfo, IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, CsrfExemptSessionAuthentication]

    def get_queryset(self):
        if self.request.query_params.get('id'):
            type = self.request.query_params.get('id')
            type_obj = Type.objects.get(pk=int(type))
            return type_obj.commody.filter(is_delete=False, is_end=False)
        else:
            return Commody.objects.filter(is_delete=False, is_end=False)


@csrf_exempt
@api_view()
def searchCommodyByNameOrDescription(request):
    '''
    根据商品名称、描述搜索商品
    :param request:
    :return:
    '''
    query_set = request.query_params.get('q')
    commody_obj = Commody.objects.filter(Q(name__icontains=query_set) | Q(description__icontains=query_set))
    commody_obj = commody_obj.filter(is_delete=False, is_end=False)
    serializer = CommodySerializer(commody_obj, many=True)
    return Response(ReturnCode(0, data=serializer.data))


class ListUpdatePersonalTransactions(mixins.ListModelMixin,
                                     mixins.UpdateModelMixin,
                                     viewsets.GenericViewSet,
                                     GetPersonal):
    lookup_field = 'pk'
    serializer_class = CommodySerializer
    permission_classes = [IsOwnerOrReadOnlyInfo, IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, CsrfExemptSessionAuthentication]

    def list(self, request, *args, **kwargs):
        '''
        列出指定用户发布的商品信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        try:
            yonghu_obj = self.get_person(request)
        except KeyError:
            return Response(ReturnCode(1, msg='must login.'), status=400)
        commody_obj = yonghu_obj.commody.filter(is_delete=False, is_end=False)
        serializer = CommodySerializer(commody_obj, many=True)
        return Response(ReturnCode(0, data=serializer.data))

    def update(self, request, *args, **kwargs):
        '''
        更新商品信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        commody_obj = self.get_object()
        # 如果是已经删除或者是已经结束的商品返回报错
        if commody_obj.is_delete:
            return Response(ReturnCode(1, msg='have already delete.'))
        data = request.data.copy()
        type_id = data.get('type_id')
        # 删除参数中指定的字段，防止框架根据参数自动修改用户不能修改的字段
        if data.get('is_delete'):
            data.pop('is_delete')
        if data.get('create_time'):
            data.pop('create_time')
        serializer = CommodySerializer(commody_obj, data=data)
        if serializer.is_valid():
            try:
                if type_id:
                    try:
                        type_new = Type.objects.get(pk=int(type_id))
                    except exceptions.ObjectDoesNotExist:
                        return Response(ReturnCode(1, msg='type objects do not exist.'))
                    commody_obj.type = type_new
                    commody_obj.save()
                serializer.save()
                return Response(ReturnCode(0, msg='success.', data=serializer.data))
            except exceptions.FieldDoesNotExist:
                return Response(ReturnCode(1, msg='qq wx and phone_number must have at least one.'))
        else:
            return Response(ReturnCode(1, msg='data invalid.'))


class ListType(mixins.ListModelMixin,
               viewsets.GenericViewSet):
    lookup_field = 'pk'
    serializer_class = TypeSerializer
    permission_classes = [IsOwnerOrReadOnlyInfo, IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, CsrfExemptSessionAuthentication]

    def get_queryset(self):
        return Type.objects.all()